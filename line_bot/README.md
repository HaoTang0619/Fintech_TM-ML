# 程式檔案解說

> 資料夾裡含有兩份文件來讓程式能在 heroku 上運行

- Procfile：heroku 執行命令，web: {語言} {檔案}，這邊語言為 python，要自動執行的檔案為 app.py，因此我們改成 **web: python app.py**。
- requirements.txt：列出所有用到的套件，heroku 會依據這份文件來安裝需要套件

## app.py (主程式)

透過修改程式裡的 handle_message() 方法內的程式碼來控制機器人的訊息回覆

### 回覆訊息

只有當有訊息傳來，才能回覆訊息
```python
line_bot_api.reply_message(reply_token, 訊息物件)
```

#### 訊息物件分類

修改範例程式碼中， handle_message() 方法內的程式碼，可實現多種功能

- TextSendMessage
- ImageSendMessage
- FlexSendMessage

## demo_ex.py

提供影片demo時使用的假範例資料。

## criminal_data.py

從資料庫抓取客戶所搜尋之資料的程式。

