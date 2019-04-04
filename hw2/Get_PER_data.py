import os
import requests
from bs4 import BeautifulSoup
from google import google
from googletrans import Translator
import sys
trans = Translator()

# Make ^C work.
import signal
def sigint_handler(signal, frame):
    print("Ctrl+C Interrupted!")
    os.kill(os.getpid(),9)
signal.signal(signal.SIGINT,sigint_handler)

print("To stop the program,type Ctrl+C.")
print("To reset output file,add an argv \"reset\".")
print("To show news content,add an argv \"show\".")

# Google search api
num_page = 10

#蘋果、自由、中時
media = [" site:appledaily.com.tw"," site:ltn.com.tw"," site:chinatimes.com"]
content = ["ndArticle_margin","text","article-body"]
word = ["人口販運","性剝削、兒童","偽造貨幣","殺人、重傷害","搶奪",
"勒贖","海盜","恐怖主義、資恐","非法販賣武器","贓物","竊盜","綁架、拘禁等妨害自由",
"環保犯罪","偽造文書","仿冒、盜版、侵害營業秘密","毒品販運","詐欺",
"走私","稅務犯罪","組織犯罪","證券犯罪","貪汙賄賂","第三方洗錢"]

os.chdir("./zh-NER-TF/")

for w in word:
	page_cnt = 0
	# Reset .txt.
	for a in sys.argv:
		if a == "reset":
			with open("../PER/" + w + ".txt","w"):
				print("Reset " + w + ".txt!")
		
	for cnt in range(len(media)):
		search_res = google.search(w + media[cnt],num_page);

		# NER
		for i in search_res:
			# If the link is valid (news sites) then get the news content,otherwise skip it.
			if(i.link == None):
				continue
			try:
				r = requests.get(i.link,timeout = 10).text
			except:
				continue
			soup = BeautifulSoup(r,"html.parser")
			tags = str(soup.find("div",content[cnt]))
			if(tags == "None"):
				continue

			# Remove noise,only keep numbers,and unicode of Chinese characters.
			t = tags.replace("「","（").replace("」","）")
			for j in range(1,129):
				if(ord("0") <= j <= ord("9")):
					continue
				t = t.replace(chr(j),"")
			t = "".join(t.split())

			# Translate to Simplified Chinese.
			try:
				t = trans.translate(t,dest = "zh-CN").text
			except:
				continue

			# Remove noise again because translate() produces some of them.
			for j in range(1,129):
				if(ord("0") <= j <= ord("9")):
					continue
				t = t.replace(chr(j),"")
			t = "".join(t.split())
			
			# Output content and results.
			try:
				os.system("python my_NER.py --mode=demo --demo_model=1521112368 --text=" + t + 
					" --word=" + w + " 1>nul 2>nul")
				with open("../PER/"+ w +".txt","r",encoding = "utf_16") as per:
					print(per.readlines()[-1])
			except:
				continue

			page_cnt += 1
			print(i.link)
			for a in sys.argv:
				if a == "show":
					print(t)
			print("\n" + w + "(page_cnt):",page_cnt,"\n")
