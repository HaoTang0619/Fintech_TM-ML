from linebot.models import *

ex_bub1 = BubbleContainer(
    direction='ltr',
    body = BoxComponent(
        layout = 'vertical',
        contents=[
            TextComponent(text='防治洗錢資料庫來源: 新聞',color='#00bfff',size='md'),
            TextComponent(text='程咬金',color='#000000',size='xxl'),
            TextComponent(text='查獲3筆資料',color='#ff0000',size='sm'),
            SeparatorComponent(margin='xl'),
            TextComponent(text='犯罪類別: 貪汙賄賂 (高風險)',color='#00bfff',size='md'),
            TextComponent(text='犯罪描述',color='#00bfff',size='md'),
            TextComponent(text='1.程咬金在今年向XX議員涉有行賄嫌疑，經...',color='#000000',size='md'),
            SeparatorComponent(margin='xl'),
            TextComponent(text='犯罪類別: 洗錢 (高風險)',color='#00bfff',size='md'), 
            TextComponent(text='犯罪描述',color='#00bfff',size='md'),
            TextComponent(text='2.經XX機關查獲，程咬金有洗錢嫌疑，...',color='#000000',size='md'),
            TextComponent(text='3.程咬金於今日被查獲有洗錢嫌疑，XX...',color='#000000',size='md'),
            SeparatorComponent(margin='xl'),
            ButtonComponent(
                style='link',
                action = URIAction(label='用google搜尋',uri='https://www.google.com/search?q=程咬金')
            )
        ]
    )
)

ex_bub2 = BubbleContainer(
    direction='ltr',
    body = BoxComponent(
    layout = 'vertical',
    contents = [TextComponent(text='查無此人相關判決',color='#000000'    ,size='md')]
    )
)

message1 = FlexSendMessage(alt_text="姓名搜尋結果", contents=ex_bub1)
message2 = FlexSendMessage(alt_text="姓名搜尋結果", contents=ex_bub2)
message3 = TextSendMessage(text='請按照以下格式查看完整內容：\n' + ('-' * 52) + '\n新聞 2\n判決 3\n' + ('-' * 52) + '\n(數字2代表第2則內容，以此類推)')
mes1 = [message1,message2,message3]


ex_bub3 = BubbleContainer(
    direction='ltr',
    body = BoxComponent(
        layout = 'vertical',
        contents=[ 
            TextComponent(text='防治洗錢資料庫來源: 新聞 or 判決',color='#00bfff',size='md'),
            TextComponent(text='滔天大罪',color='#000000',size='xxl'),
            TextComponent(text='顯示隨機5筆姓名',color='#ff0000',size='sm'),
            SeparatorComponent(margin='xl'),
            ButtonComponent(style='link', action = MessageAction(label='陳XX',text='查姓名 陳XX')),
            ButtonComponent(style='link', action = MessageAction(label='王XX',text='查姓名 王XX')),
            ButtonComponent(style='link', action = MessageAction(label='李XX',text='查姓名 李XX')),
            ButtonComponent(style='link', action = MessageAction(label='吳XX',text='查姓名 吳XX')),
            ButtonComponent(style='link', action = MessageAction(label='林XX',text='查姓名 林XX')),
            SeparatorComponent(margin='xl'),
            ButtonComponent(style='link', action = URIAction(label='用google搜尋',uri='https://www.google.com/search?q=滔天大罪')),
            ButtonComponent(style='link', action = URIAction(label='完整人名列表(靜態)',uri='https://www.csie.ntu.edu.tw/~b06902020/name_list/滔天大罪_list.txt'))
        ]
    )
)
mes2 = FlexSendMessage(alt_text="姓名搜尋結果", contents=ex_bub3)
