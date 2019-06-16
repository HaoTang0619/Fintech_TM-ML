# coding=UTF-8
import re, pymysql, os, pickle
import pandas as pd
from collections import Counter

keywords = ['人口販運', '性剝削', '偽造貨幣', '殺人', '重傷害', '搶奪' , '勒索' , '海盜', '恐怖主義', '資恐', '非法販運武器'
            , '贓物', '竊盜', '綁架', '拘禁', '妨礙自由', '環保犯罪', '偽造文書', '仿冒', '侵害商業秘密', '毒品犯運', '詐欺'
            , '走私', '稅務犯罪', '組織犯罪', '證卷犯罪', '貪汙賄賂', '洗錢']

def get_data_from_sql(table_name, keyword, keyword_type):
	# 略過這個
    contents_list=[]
    db = pymysql.connect(host="18.217.252.187",port=3306, user="public_author",passwd="antimoneylaunderingisgood2",db="AML_News",charset='utf8')
    try:
        with db.cursor() as cursor:
            sql0 = "SELECT * FROM `" + table_name + "` WHERE '" + keyword +"' LIKE CONCAT('%', `" + keyword_type + "`, '%')"
            cursor.execute(sql0)
            contents_list = cursor.fetchall()
        db.commit()
    finally:
        db.close()
    return contents_list

class Criminal:
    def __init__(self, criminal_name):
    	# 你需要的東西在這裡，可以看 main 裡面的操作
        self.criminal_name = criminal_name
        self.crime_news = {}
        # format:
        # {	crime1: [news1, news2, news3]],
        # 	crime2: [news1, news2, news3]],
        # 	crime3: [news1, news2, news3]], ...}
        self.crime_judical = {}
        # format:
        # {	crime1: [news1, news2, news3]],
        # 	crime2: [news1, news2, news3]],
        # 	crime3: [news1, news2, news3]], ...}
        self._update_news_data()
        self._update_judical_data()
    def _update_news_data(self):
        sql_data = get_data_from_sql('apple_daily_people', self.criminal_name, 'name')
        output_dataframe = pd.DataFrame(list(sql_data), columns=['name','article','keyword'])
        for idx in range(len(output_dataframe)):
            if output_dataframe['keyword'][idx] in self.crime_news:
                self.crime_news[output_dataframe['keyword'][idx]].append(output_dataframe['article'][idx])
            else:
                self.crime_news[output_dataframe['keyword'][idx]] = [output_dataframe['article'][idx]]
        return
    def _update_judical_data(self):
        sql_data = get_data_from_sql('judical_criminal_people', self.criminal_name, 'name')
        output_dataframe = pd.DataFrame(list(sql_data), columns=['id','name','article','keyword'])
        for idx in range(len(output_dataframe)):
            if output_dataframe['keyword'][idx] in self.crime_judical:
                self.crime_judical[output_dataframe['keyword'][idx]].append(output_dataframe['article'][idx])
            else:
                self.crime_judical[output_dataframe['keyword'][idx]] = [output_dataframe['article'][idx]]
        return

def get_popular_criminal_rank(keyword, num=0, force_update=False):
    # 返回一個list，裡面是那個犯罪的前幾名熱門人選
    # ex: 
    #     get_popular_criminal_rank('人口販運', 3)
    #     return [('提勒森', 5), ('彭立光', 3), ('余孝祖', 3)]
    # keywords = ['人口販運', '性剝削', '偽造貨幣', '殺人', '重傷害', '搶奪' , '勒索' , '海盜', '恐怖主義', '資恐', '非法販運武器'
    #             , '贓物', '竊盜', '綁架', '拘禁', '妨礙自由', '環保犯罪', '偽造文書', '仿冒', '侵害商業秘密', '毒品犯運', '詐欺'
    #             , '走私', '稅務犯罪', '組織犯罪', '證卷犯罪', '貪汙賄賂', '洗錢']
    # num:          要拿前幾名的資料，預設為0，0的時候全輸出
    # force_update: 強制更新本地檔案，資料庫更新時使用。
    sorted_data = None
    if os.path.exists('%s_ranking.pkl'%(keyword)) and not force_update:
    	# get from local cache
        with open('%s_ranking.pkl'%(keyword), 'rb') as fp:
            sorted_data = pickle.load(fp)
    else:
    	# get from sql
        all_names = []
        # news data
        sql_data = get_data_from_sql('apple_daily_people', keyword, 'keyword')
        output_dataframe = pd.DataFrame(list(sql_data), columns=['name','article','keyword'])
        all_names += list(output_dataframe['name'])
        # judical data
        sql_data = get_data_from_sql('judical_criminal_people', keyword, 'keyword')
        output_dataframe = pd.DataFrame(list(sql_data), columns=['id','name','article','keyword'])
        all_names += list(output_dataframe['name'])
        # sorted
        sorted_data = Counter(all_names)
        with open('%s_ranking.pkl'%(keyword), 'wb') as fp:
            pickle.dump(sorted_data, fp)
    if num > 0:
        return sorted_data.most_common(num)
    else:
        return sorted_data.most_common()

if __name__ == '__main__':
    myCriminal = Criminal('提勒森')
    print('in myCriminal.crime_news')
    for key, items in myCriminal.crime_news.items():
        print('====', key, '====')
        for item in items:
            print(item[:30])
    print('in myCriminal.crime_judical')
    for key, items in myCriminal.crime_judical.items():
        print('====', key, '====')
        for item in items:
            print(item[:30])
    print('get top 10 frequency crimes')
print(get_popular_criminal_rank('人口販運', 10))
