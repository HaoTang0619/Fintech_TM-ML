import os
import requests
from bs4 import BeautifulSoup
from google import google
from googletrans import Translator
import sys
trans = Translator()

# Reset PER.txt.
if len(sys.argv) > 1 and sys.argv[1] == "del":
	with open("PER.txt","w"):
		print("Reset PER.txt!")

# Google search api
num_page = 5

media = [" site:appledaily.com.tw"]
content = ["ndArticle_margin"]
word = ["金融犯罪","洗錢嫌犯"]

search_res = google.search(word[1] + media[0],num_page);

# NER
os.chdir("./zh-NER-TF/")
for i in search_res:
	# If the link is valid (news sites) then get the news content,otherwise skip it.
	print(i.link)
	if(i.link == None):
		continue
	r = requests.get(i.link).text
	soup = BeautifulSoup(r,"html.parser")
	tags = str(soup.find("div",content[0]))
	if(tags == "None"):
		continue

	# Remove noise,only keep numbers,and unicode of Chinese characters.
	t = tags.replace("「","（").replace("」","）")
	for j in range(1,129):
		if(ord("0") <= j <= ord("9")):
			continue
		t = t.replace(chr(j),"")
	t = "".join(t.split())
	
	# 篩記者
	start = t.find("報導】")
	if start == -1:
		start = -3

	# Translate to Simplified Chinese.
	# Max translation length seems to be 1783.
	t = trans.translate(t[start + 3:1200],dest = "zh-CN").text
	
	# Remove noise again because translate() produces some of them.
	for j in range(1,129):
		if(ord("0") <= j <= ord("9")):
			continue
		t = t.replace(chr(j),"")
	t = "".join(t.split())
	
	# Output content and results.
	print(t)
	os.system("python my_NER.py --mode=demo --demo_model=1521112368 --text=" + t + " 1>nul 2>nul")
	with open("../PER.txt","r",encoding = "utf_16") as per:
		print(per.readlines()[-3:])
