#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import pymysql, time, re, json, requests, threading
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
#這個cell是我為你們寫好的function

def Sent_Data_To_Mysql(name, article, keyword, table_name):
    db = pymysql.connect(host="18.217.252.187",port=3306, user="public_author",passwd="antimoneylaunderingisgood2",db="AML_News" ,charset='utf8')
    content = db.escape_string(article)
    try:
        with db.cursor() as cursor:
            sql0 = "SELECT `id` FROM `"+table_name+"` WHERE '"+article+"' LIKE CONCAT('%', `article`, '%')"
            cursor.execute(sql0)
            duplicate_id = cursor.fetchone()
            if(duplicate_id is not None):#如果已經存在一個content重複的
                sql1 = " INSERT INTO `"+table_name+"` (`id`, `name`,`article`,`keyword`) VALUES (%s,%s,%s,%s) "
                sql2 = " ON DUPLICATE KEY UPDATE `article`= VALUES(`article`),`name`= VALUES(`name`),`keyword`= VALUES(`keyword`)"
                cursor.execute(sql1+sql2, (str(duplicate_id[0]),name,article,keyword))
                #print(str(duplicate_id[0]))
            else:#如果沒有重複的
                sql = "INSERT INTO `"+table_name+"`(`article`,`name`,`keyword`) VALUES ( %s,%s,%s)"
                cursor.execute(sql, (article,name,keyword))
        db.commit()
    finally:
        db.close()

def Get_Data_From_Mysql(table_name,keyword):
    contents_list=[]
    target_ids =[]
    db = pymysql.connect(host="18.217.252.187",port=3306, user="public_author",passwd="antimoneylaunderingisgood2",db="AML_News" ,charset='utf8')
    try:
        with db.cursor() as cursor:
            if(keyword=="all"):
                sql0 = "SELECT * FROM `"+table_name+"`"
                cursor.execute(sql0)
                contents_list = cursor.fetchall()
            else: 
                sql0 = "SELECT * FROM `"+table_name+"` WHERE '"+keyword+"' LIKE CONCAT('%', `keyword`)"
                cursor.execute(sql0)
                contents_list = cursor.fetchall()
                
        db.commit()
    finally:
        db.close()
    return  pd.DataFrame(list(contents_list), columns=['id','name','article','keyword'])

#檢查是否為最後一頁，輸入keyword後檢索結果頁面右上角會有第幾頁，共幾頁的資料
def get_final_page(s):
    a = s.replace(' ', '').split('/')[1]
    a = int(a.split('頁')[0])
    return (a if a < 25 else 25)

def crawl_crimeLinkList_by_crimeKeyword(crime_keyword):
    my_options = Options()
    my_options.add_argument("--headless")
    my_options.add_argument('log-level=3')
    main_driver = webdriver.Chrome('chromedriver.exe', chrome_options=my_options)
    main_driver.implicitly_wait(10)
    main_driver.get('https://law.judicial.gov.tw/FJUD/defaulte.aspx')

    #簡單檢所的頁面中，輸入關鍵字，這邊你們可以放入洗錢嫌疑程度的關鍵字
    keyword_input_ele = main_driver.find_element_by_xpath('//*[@id="txtKW"]')
    keyword_input_ele.send_keys(crime_keyword)

    btn_ele = keyword_input_ele.find_element_by_xpath('//*[@id="btnSimpleQry"]')
    btn_ele.click()
    #這邊很重要，要切換到iframe內
    main_driver.switch_to.frame("iframe-data")
    case_link_list=[]
    #print(main_driver.current_url, '--1--')
    try:
        final_page_num = get_final_page(main_driver.find_element_by_xpath('//*[@id="plPager"]/span[1]').text)
    except:
        final_page_num = 1
    #print(main_driver.current_url, '--2--')
    for i in range(final_page_num):
        #print(main_driver.current_url)
        ##取的一頁中的所有檢索案件
        case_list = main_driver.find_elements_by_id('hlTitle')
        for idx, case in enumerate(case_list):
            link = case.get_attribute('href')
            # print(link)
            case_link_list.append(link)#將每個案件的檢索結果頁面連結放在case_link_list中
        #注意因為網頁最多只會提供500比檢索資料，因此case_link_list長度最多500
        #如果是最後一頁，就跳出
        if i != final_page_num-1:
            next_page = main_driver.find_element_by_id('hlNext').get_attribute("href")
            main_driver.get(next_page)
    main_driver.quit()
    return case_link_list

#注意在第11行，找到有"被　　　告"的關鍵字之後就開始搜尋這個項目裡的名子，直到
#第12行的「謝○○」為止
def get_defendantName(line_string):
    line_string = line_string.replace(')', '）')
    line_string = line_string.replace(':', '：')
    #print(line_string)
    output=''
    for start_target in ["被  告","被   告","即 被 告", "被移送人","即被移送人"]:
        if(line_string.find(start_target)!= -1):
            line_split = line_string.split()
            if len(line_split) < 2: continue
            output = line_split[-1].strip()
            if 2 < len(output) < 5:
                return output, True
            elif len(output) > 5:
                idxr = output.find('）')
                if idxr == -1 or (output.find("負責人") == -1): continue
                elif (output.find('：') != -1):
                    return output[output.find('：')+1:idxr], True
                else:
                    return output[idxr-3:idxr], True
    return output, False

#做把各篇判決書內的被告取出名子的方法
def get_Name_List(context, case_link):
    temp = pd.DataFrame(columns=['名稱','正文'])
    #先把判決書的每行分開
    lines = context.split('\n')
    context = context + "\nlink: {0}".format(case_link)
    #接著對判決書內的每行做處理
    find_defendantName = False
    for line in lines[:10]:
        defendantName, status = get_defendantName(line)
        if status and (defendantName.find('○') == -1) and (defendantName.find('') == -1):
            #print('->', defendantName)
            temp = temp.append({'名稱':defendantName,'正文':context}, ignore_index=True)
            find_defendantName = True
            break
    if find_defendantName:
        return temp
    else:
        return None

def crawl_crimeDf_by_crimeLinkList(case_link_list):
    my_options = Options()
    my_options.add_argument("--headless")
    my_options.add_argument('log-level=3')
    main_driver = webdriver.Chrome('chromedriver.exe', chrome_options=my_options)
    main_driver.implicitly_wait(10)
    df = pd.DataFrame(columns=['名稱','正文'])
    for case_link in case_link_list:
        #print("----")
        if(case_link==None): continue 
        #----------------這邊從每篇判決書文字中取得我們要的人名------------------#
        main_driver.get(case_link)
        case_text = main_driver.find_element_by_class_name('text-pre').text.replace('\u3000', ' ').replace('\'', ' ')
        case_text = case_text[:case_text.find('書記官')]
        #if len(case_text) > 2000:
        #    continue
        sub_df = get_Name_List(case_text, case_link)
        if sub_df is not None:
            df = df.append(sub_df)
        #time.sleep(1)
        #-------------------------------------------------------------------#
    #變成dataframe方便之後處理，接下來就是上傳到資料庫啦~
    df = df.reset_index(drop=True)#把index重新整理
    main_driver.quit()
    return df

def agentWork(words, agentIdx):
    print(words)
    for crime_keyword in words:
        print(' ----- %s start -----'%(crime_keyword))
        crimeLinkList = crawl_crimeLinkList_by_crimeKeyword(crime_keyword)
        #print(crimeLinkList)
        crimeDf = crawl_crimeDf_by_crimeLinkList(crimeLinkList)
        # print(crimeContent)
        org_filter_list = ['公司','委員會','基金會']
        #將公司跟人名分開
        df_org = crimeDf[crimeDf['名稱'].str.contains('|'.join(org_filter_list))]
        df_people = crimeDf[~crimeDf['名稱'].str.contains('|'.join(org_filter_list))]
        #print(df_people)
        # break
        #df_people.to_csv('judicial%s.csv'%(crime_keyword))
        for index, row in df_people.iterrows():
            #print(row['名稱'], len(row['正文']))
            #print(row['正文'])
            #print(len(row['正文']))
            Sent_Data_To_Mysql(row['名稱'],row['正文'],crime_keyword,'judical_criminal_people')
    return

if __name__ == '__main__':
    words = ['人口販運', '性剝削', '偽造貨幣', '殺人', '重傷害', '搶奪' , '勒索' , '海盜', '恐怖主義', '資恐', '非法販運武器'
            , '贓物', '竊盜', '綁架', '拘禁', '妨礙自由', '環保犯罪', '偽造文書', '仿冒', '侵害商業秘密', '毒品犯運', '詐欺'
            , '走私', '稅務犯罪', '組織犯罪', '證卷犯罪', '貪汙賄賂', '洗錢']
    #words = [['綁架','綁架'],['有價證券','證卷犯罪'],['貪汙','貪汙賄賂'],['賄賂','貪汙賄賂']]
    agentList = []
    agetNum = 2
    for i in range(agetNum):
        agent = threading.Thread(target=agentWork, args=[words[len(words)//agetNum*(i):len(words)//agetNum*(i+1)], i])
        agent.start()
        agentList.append(agent)
    for i in range(agetNum):
        agentList[i].join()
    print("---- end ----")