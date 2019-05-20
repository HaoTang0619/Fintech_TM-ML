from opencc import OpenCC
from nltk.parse.stanford import StanfordParser
from nltk.tokenize import StanfordSegmenter
from nltk.tag import StanfordNERTagger
from nltk.tag import StanfordPOSTagger
import pickle, re, pymysql, jieba, os
import pandas as pd

chi_tagger = StanfordPOSTagger('./StanfordNLP/models/chinese-distsim.tagger',
							   './StanfordNLP/jars/stanford-ner.jar')
segmenter = StanfordSegmenter(
	java_class='edu.stanford.nlp.ie.crf.CRFClassifier',
	path_to_jar="./StanfordNLP/jars/stanford-segmenter-3.9.2.jar",
	path_to_slf4j="./StanfordNLP/jars/slf4j-api.jar",
	path_to_sihan_corpora_dict="./StanfordNLP/stanford-segmenter-2018-10-16/data",
	path_to_model="./StanfordNLP/stanford-segmenter-2018-10-16/data/pku.gz",
	path_to_dict="./StanfordNLP/stanford-segmenter-2018-10-16/data/dict-chris6.ser.gz"
)

os.environ["JAVA_HOME"] = "/tmp2/b05902109/jdk-12.0.1"#注意這邊你們電腦要安裝java jdk，並放入你們自己的jdk的安裝路徑
os.environ["CLASSPATH"] = "./StanfordNLP/stanford-parser-2018-10-17"
os.environ["STANFORD_MODELS"] = "./StanfordNLP/models"

ch_parser = StanfordParser(model_path='./StanfordNLP/models/chinesePCFG.ser.gz')
cc = OpenCC('t2s')  # (Optional )convert from Simplified Chinese to Traditional Chinese

def Get_Data_From_Mysql(source_name,keyword):
	contents_list=[]
	target_ids =[]
	db = pymysql.connect(host="18.217.252.187",port=3306, user="public_author",passwd="antimoneylaunderingisgood2",db="AML_News" ,charset='utf8')
	try:
		with db.cursor() as cursor:
			if(keyword=="all"):
				sql0 = "SELECT * FROM `"+source_name+"`"
				cursor.execute(sql0)
				contents_list = cursor.fetchall()
			else: 
				sql0 = "SELECT * FROM `"+source_name+"` WHERE '"+keyword+"' LIKE CONCAT('%', `keyword`)"
				cursor.execute(sql0)
				contents_list = cursor.fetchall()
				
		db.commit()
	finally:
		db.close()
	return  pd.DataFrame(list(contents_list), columns=['id','tagged_article','tag_type','keyword'])

def get_tagged_and_untagged_sentences(tagged_article):
	sentences_and_nameIdxs = []
	tagged_article = tagged_article.replace('\n', '').replace(' ', '').replace('。', '。\a').replace('《', '').replace('》', '').replace('（）', '').split('\a')
	for tagged_sentence in tagged_article:
		if tagged_sentence.find('/nr') < 0:
			continue
		untagged_sentence = tagged_sentence.replace('/nr', '').replace('/nt', '').replace('/ns', '').replace('/o', '')
		name_list = []
		for findIter in re.finditer('/nr', tagged_sentence):
			start_idx = tagged_sentence[:findIter.start()].rfind('/o') + 2
			end_idx = findIter.start()
			name = tagged_sentence[start_idx:end_idx]
			if name not in name_list:
				name_list.append(name)
		names_and_idxs = []
		for name in name_list:
			name_and_idx = [name]
			for findIter in re.finditer(name, untagged_sentence):
				name_and_idx.append([findIter.start(), findIter.end()])
			names_and_idxs.append(name_and_idx)
		sentences_and_nameIdxs.append([tagged_sentence, untagged_sentence, names_and_idxs])
	return sentences_and_nameIdxs

def keep_name_right(tagged_sentence):
	"""
	用tag過NER的句子斷句
	再把每一個斷詞送進結巴切詞
	希望盡可能保持姓名完整
	EX:
	input: 阮/nr 姓女子為首的/o 偽鈔集團/nt ，該集團今年二月已被/o 雲林/ns 警方偵破，
	ouput(用結巴斷詞) >> 阮, 姓, 女子, 為首, 的, 偽鈔, 集團, ... 
	"""
	global cc
	word_list = []
	subString_list = []
	subString_list_tmp = tagged_sentence.replace('ns', '').replace('nt', '').replace('o', '').split('/')
	for idx in range(len(subString_list_tmp)):
		if idx == 0:
			continue
		if subString_list_tmp[idx][:2] == 'nr':
			subString_list.append([subString_list_tmp[idx - 1], True])
			subString_list_tmp[idx] = subString_list_tmp[idx].replace('nr', '')
		else:
			if len(subString_list) == 0:
				subString_list.append([subString_list_tmp[idx - 1], False])
			elif subString_list[-1][1] == True:
				subString_list.append([subString_list_tmp[idx - 1], False])
			else:
				subString_list[-1][0] += subString_list_tmp[idx - 1]

	if subString_list[-1][1] == True:
		subString_list.append([subString_list_tmp[-1], False])
	else:
		subString_list[-1][0] += subString_list_tmp[-1]

	for subString, is_nr in subString_list:
		#print(is_nr, subString)
		if is_nr:
			word_list.append(cc.convert(subString))
		else:
			subString_simpleZh = cc.convert(subString)#一樣轉成簡體字，這樣Stanford的系統才會比較準確
			word_list += list(jieba.cut(subString_simpleZh, cut_all=False))
	#print(word_list)
	return word_list

def create_tree_and_save_it(tagged_article, crime_name, file):
	#跑文法樹
	#sentences: 保有NER tag
	#sentence: 原型句子
		#name_and_idx: 姓名、位置
	global ch_parser
	tagged_and_untagged_sentences = get_tagged_and_untagged_sentences(tagged_article)
	for tagged_sentence, untagged_sentence, names_and_idxs in tagged_and_untagged_sentences:
		#print(tagged_sentence)
		#print(untagged_sentence)
		#print(names_and_idxs)
		if crime_name == '證卷犯罪':
			crime_name = '證券犯罪'
		if crime_name in untagged_sentence and len(untagged_sentence) < 500: #如果犯罪名稱有在句子裡
			word_list = keep_name_right(tagged_sentence)
			sent = ch_parser.parse(word_list) #形成文法樹
			pickle.dump(sent, file) #用pickle存
			pickle.dump(names_and_idxs, file)
		else:
			continue
	return

if __name__ == '__main__':
	source_names = ['apple_daily','china_times', 'liberty_times', 'united_daily']
	# output_dataframe = Get_Data_From_Mysql(source_name[0],'all') #洗錢為例
	crime_names = ['人口販運', '性剝削', '偽造貨幣', '殺人', '重傷害', '搶奪' , '勒索' , '海盜', '恐怖主義', '資恐', '非法販運武器', 
					'贓物', '竊盜', '綁架', '拘禁', '妨礙自由', '環保犯罪', '偽造文書', '仿冒', '侵害商業秘密', '毒品犯運', '詐欺', 
					'走私', '稅務犯罪', '組織犯罪', '證卷犯罪', '貪汙賄賂', '洗錢']
	#篩選句子內有犯罪名稱的句子
	for crime_name in crime_names:
		print('----- crime_name: ', crime_name, ' start -----')
		fileName = crime_name + '.pkl'
		f = open(fileName, 'wb')
		for source_name in source_names:
			print('----- source_name: ', source_name, ' start -----')
			output_dataframe = Get_Data_From_Mysql(source_name, crime_name)
			crime_idx = (output_dataframe['keyword'] == crime_name) #####這裡要改，(舉洗錢為例)
			for tagged_article in output_dataframe[crime_idx]["tagged_article"]: #####可以像我先跑個幾筆([0:10])試一下，再跑全部，全部就是直接跑 >> for i in database
				create_tree_and_save_it(tagged_article, crime_name, f)   #####這裡要改，(舉洗錢為例)
		f.close()