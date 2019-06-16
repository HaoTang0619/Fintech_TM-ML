from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import random
import os

import criminal_data as crida

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('iQYo262WUqoCx3fP+1OTHVCl7EpUgTv4eG8oQZVbupv1Vz9k08ytnW4+7orj1/VftxQkM3TfrXNC5YHTKv1jLhIpfxU8Odot7G/KEd73YhmCbBz57jFe5Xo5xTxq67N7hJpl0VT/cJFnqHhXsJPoWAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('dac067c748c3e48b504f313170ef42c1')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

keywords = {'人口販運':'(低風險)', '性剝削':'(低風險)', '偽造貨幣':'(低風險)', '殺人':'(低風險)', '重傷害':'(低風險)', '搶奪':'(低風險)', '勒索':'(低風險)', '資恐':'(低風險)', '非法販運武器':'(中風險)', '贓物':'(中風險)', '竊盜':'(中風險)', '綁架':'(中風險)', '拘禁':'(中風險)', '妨礙自由':'(中風險)', '環保犯罪':'(中風險)', '偽造文書':'(中風險)', '仿冒':'(高風險)', '侵害商業秘密':'(高風險)', '毒品販運':'(高風險)', '詐欺':'(高風險)', '走私':'(高風險)', '稅務犯罪':'(高風險)', '組織犯罪':'(高風險)', '證券犯罪':'(高風險)', '貪汙賄賂':'(高風險)', '洗錢':'(高風險)'}

fig = {'ALL':'ALL', '低風險':'low', '中風險':'mid', '高風險':'high'}
fig_url = 'https://raw.githubusercontent.com/howard919901/Data_for_line/master/Figures/'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    received = event.message.text
    if '查姓名 ' == received[0:4] :
        os.system("rm -f ./data_*")
        name = received[4:].split()[0]
        if name == "程咬金":
            import demo_ex as dex
            mes = dex.mes1
            line_bot_api.reply_message(event.reply_token, mes)
            return
        
        myCriminal = crida.Criminal(name)
        con_tmp = []
        tmp_flag = 0
        flag = 1
        cnt = 0
        for key, items in myCriminal.crime_news.items():
            if key == "毒品犯運":
                key = "毒品販運"
            if key == "證卷犯罪":
                key = "證券犯罪"
            risk = keywords[key]
            if flag == 1:
                con_tmp = [ 
                    TextComponent(text='防治洗錢資料庫來源: 新聞',color='#00bfff',size='md'),
                    TextComponent(text=name,color='#000000',size='xxl'),
                    SeparatorComponent(margin='xl')
                ]
                flag = 0
            con_tmp.append(TextComponent(text='犯罪類別: ' + str(key) + ' ' + risk,color='#00bfff',size='md'))
            con_tmp.append(TextComponent(text='新聞描述',color='#00bfff',size='md'))
            for item in items:
                cnt += 1
                con_tmp.append(TextComponent(text=str(cnt) + ". " + item[:30],color='#000000',size='md'))
                with open('./data_new_' + str(cnt),'w') as dan:
                    dan.write(item)
            con_tmp.append(SeparatorComponent(margin='xl'))
        
        if len(con_tmp):
            con_tmp.append(ButtonComponent(style='link', action = URIAction(label='用google搜尋',uri='https://www.google.com/search?q=' + name)))
            con_tmp.insert(2,TextComponent(text='查獲' + str(cnt) + '筆資料',color='#ff0000',size='sm'))
        else :
            tmp_flag = 1
            con_tmp = [TextComponent(text='查無此人相關新聞',color='#000000',size='md')]

        bub1 = BubbleContainer(
            direction='ltr',
            body = BoxComponent(
                layout = 'vertical',
                contents = con_tmp
            )
        )
        message1 = FlexSendMessage(alt_text="姓名搜尋結果", contents=bub1)

        con_tmp = []
        flag = 1
        cnt = 0
        for key, items in myCriminal.crime_judical.items():
            if key == "毒品犯運":
                key = "毒品販運"
            if key == "證卷犯罪":
                key = "證券犯罪"
            risk = keywords[key]
            if flag == 1:
                con_tmp = [ 
                    TextComponent(text='防治洗錢資料庫來源: 判決',color='#00bfff',size='md'),
                    TextComponent(text=name,color='#000000',size='xxl'),
                    SeparatorComponent(margin='xl')
                ]
                flag = 0
            con_tmp.append(TextComponent(text='犯罪類別: ' + str(key) + ' ' + risk,color='#00bfff',size='md'))
            con_tmp.append(TextComponent(text='判決描述',color='#00bfff',size='md'))
            for item in items:
                cnt += 1
                con_tmp.append(TextComponent(text=str(cnt) + ". " + item[:30],color='#000000',size='md'))
                with open('./data_jud_' + str(cnt),'w') as daj:
                    daj.write(item)
            con_tmp.append(SeparatorComponent(margin='xl'))
        
        if len(con_tmp):
            con_tmp.append(ButtonComponent(style='link', action = URIAction(label='用google搜尋',uri='https://www.google.com/search?q=' + name)))
            con_tmp.insert(2,TextComponent(text='查獲' + str(cnt) + '筆資料',color='#ff0000',size='sm'))
        else :
            if tmp_flag:
                tmp_flag = 2
            con_tmp = [TextComponent(text='查無此人相關判決',color='#000000',size='md')]
        
        bub2 = BubbleContainer(
            direction='ltr',
            body = BoxComponent(
                layout = 'vertical',
                contents = con_tmp
            )
        )
        message1 = FlexSendMessage(alt_text="姓名搜尋結果", contents=bub1)
        message2 = FlexSendMessage(alt_text="姓名搜尋結果", contents=bub2)
        message3 = TextSendMessage(text='請按照以下格式查看完整內容：\n' + ('-' * 52) + '\n新聞 2\n判決 3\n' + ('-' * 52) + '\n(數字2代表第2則內容，以此類推)') 
        mes = [message1,message2]
        if tmp_flag != 2:
            mes.append(message3)
        line_bot_api.reply_message(event.reply_token, mes)
    
    elif 'Search by name' == received :
        message = TextSendMessage(text='請按照以下格式輸入以搜尋：\n' + ('-' * 48) + '\n查姓名 你想查詢的姓名\n' + ('-' * 48) + '\n範例圖片如下：') 
        image_url = fig_url + 'ex_name.jpg'
        example = ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)
        line_bot_api.reply_message(event.reply_token, [message, example])
    
    elif '查罪名 ' == received[0:4] :
        crime = received[4:].split()[0]
        if crime == '滔天大罪':
            import demo_ex as dex
            mes = dex.mes2
            line_bot_api.reply_message(event.reply_token, mes)
            return

        if crime not in keywords:
            error = TextSendMessage(text='不支援此罪名。')
            line_bot_api.reply_message(event.reply_token, error)
            return
        con_tmp = [ 
                    TextComponent(text='防治洗錢資料庫來源: 新聞 or 判決',color='#00bfff',size='md'),
                    TextComponent(text=crime,color='#000000',size='xxl'),
        ]
        if crime == "毒品販運":
            crime = "毒品犯運"
        if crime == "證券犯罪":
            crime = "證卷犯罪"
        res = crida.get_popular_criminal_rank(crime,0)
        con_tmp.append(TextComponent(text='顯示隨機' + str(min(5,len(res))) + '筆姓名',color='#ff0000',size='sm'))
        con_tmp.append(SeparatorComponent(margin='xl'))
        random.shuffle(res)
        for i in res[:5]:
            con_tmp.append(ButtonComponent(style='link', action = MessageAction(label=i[0],text='查姓名 ' + i[0])))
        con_tmp.append(SeparatorComponent(margin='xl'))
        con_tmp.append(ButtonComponent(style='link', action = URIAction(label='用google搜尋',uri='https://www.google.com/search?q=' + crime)))
        con_tmp.append(ButtonComponent(style='link', action = URIAction(label='完整人名列表(靜態)',uri='https://www.csie.ntu.edu.tw/~b06902020/name_list/' + crime + '_list.txt')))

        bubble = BubbleContainer(
            direction='ltr',
            body = BoxComponent(
                layout = 'vertical',
                contents=con_tmp
            )
        )
        message = FlexSendMessage(alt_text="罪名搜尋結果", contents=bubble)
        line_bot_api.reply_message(event.reply_token, message)
    
    elif 'Search by crime' == received :
        message = TextSendMessage(text='請按照以下格式輸入以搜尋：\n' + ('-' * 48) +'\n查罪名 你想查詢的罪名\n' + ('-' * 48) + '\n目前支援罪名：\n{人口販運, 性剝削, 偽造貨幣, 殺人, 重傷害, 搶奪, 勒索, 資恐, 非法販運武器, 贓物, 竊盜, 綁架, 拘禁, 妨礙自由, 環保犯罪, 偽造文書, 仿冒, 侵害商業秘密, 毒品販運, 詐欺, 走私, 稅務犯罪, 組織犯罪, 證券犯罪, 貪汙賄賂, 洗錢}\n\n範例圖片如下：') 
        image_url = fig_url + 'ex_crime.jpg'
        example = ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)
        line_bot_api.reply_message(event.reply_token, [message, example])
    
    elif '共現圖 ' == received[0:4] :
        figure = received[4:].split()[0]
        if figure not in fig:
            error = TextSendMessage(text='不支援此風險程度。')
            line_bot_api.reply_message(event.reply_token, error)
            return
        img1_url = fig_url + fig[figure] + '_1.png'
        fig1 = ImageSendMessage(original_content_url=img1_url, preview_image_url=img1_url)
        img2_url = fig_url + fig[figure] + '_2.png'
        fig2 = ImageSendMessage(original_content_url=img2_url, preview_image_url=img2_url)
        line_bot_api.reply_message(event.reply_token, [fig1, fig2])
    
    elif 'Figure of crime' == received :
        message = TextSendMessage(text='請按照以下格式輸入以查看圖片：\n' + ('-' * 56) +'\n共現圖 你想查看的風險程度\n' + ('-' * 56) + '\n目前支援風險程度：\n{ALL, 低風險, 中風險, 高風險}\n\n系統會同時輸出共現圖和熱點圖\n\n範例圖片如下：') 
        image_url = fig_url + 'ex_figure.jpg'
        example = ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)
        line_bot_api.reply_message(event.reply_token, [message, example])
    
    elif '新聞 ' == received[0:3]: 
        idx = received[3:].split()[0]
        t = '不存在這則新聞。'
        if os.path.isfile("./data_new_" + idx):
            with open("./data_new_" + idx) as dan:
                t = dan.read()
        message = []
        tex = 0
        while tex < len(t):
            message.append(TextSendMessage(text = t[tex:tex+1900]))
            tex += 1900
        line_bot_api.reply_message(event.reply_token, message)
    
    elif '判決 ' == received[0:3]: 
        idx = received[3:].split()[0]
        t = '不存在這則判決。'
        if os.path.isfile("./data_jud_" + idx):
            with open("./data_jud_" + idx) as daj:
                t = daj.read().split('link:')[0]
        message = []
        tex = 0
        while tex < len(t):
            message.append(TextSendMessage(text = t[tex:tex+1900]))
            tex += 1900
        line_bot_api.reply_message(event.reply_token, message)


    else :
        message = TextSendMessage(text='I\'m Patrick !')
        patrick = TextSendMessage(text='輸入「派大星」獲得更多資訊......')
        # line_bot_api.reply_message(event.reply_token, [message, patrick])

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
