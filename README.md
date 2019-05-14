# Fintech_TM&ML

國立台灣大學 管理學院 財務金融學研究所

107-2【金融科技-文字探勘與機器學習】

b05902109 資工三 柯上優

## Hw0

- Level 1: 流程圖	√ finish
- Level 2: 註解		√ finish
- Level 3: 修改

## Hw1

- ETF 爬蟲解說
  - 請各組在所指定的 ETF 資料中，先篩選出於 2015 年年底前既已存在的 ETF(可從 EXCEL 檔中的 W 欄看到時間)。(原先說要特地存成一個 excel 檔案就不用了)
  - 承上，請利用爬蟲方法整理出上述篩選後的 ETF 集合中，其每一檔 ETF 的每日收盤價，時間範圍從該 ETF 於 2015 年年底最後一個交易日起至程式執行的當下(Now()函數)，將每日的資料都抓下來，不需要分月底或三個月(這樣對你們來說比較簡單)。並將整理好的資料彙整在 pandas 的 dataframe 中，如圖 1 顯示，橫軸為 ETF 資料(標頭為「該ETF 名稱」)，縱軸為年-月-日(格式是 Python 的 Datetime ‘yyyy-mm-dd’) ，標頭為「Date」。如果該 ETF 在該時間沒有資料就空白。如果是用 Jupyter 的人請執行完後搭配執行結果將.ipynb 檔上傳 GitHub 這樣方便助教我檢查是否有完成，如果不是的也請在 Github 上放一個執行後的截圖。
  - 如果該 ETF 的 Home page 沒有讓你下載每日收盤價的連結的話，請到 Yahoo Finance 輸入你 ETF 的名稱後找尋資料https://finance.yahoo.com/，以「Adj Close**」為準，但希望大家還是先以 Homepage 為主。如果以上方法都不行，請將該 ETF 紀錄在 HW1 資料夾內的 README.md 中，標記為「無法完成的 ETF 名稱」
  - 在 GitHub README.md 上要寫的教學文件必須包含下面內容:
    1.你選擇用甚麼樣的套件來做網路爬蟲?為什麼要用這個套件
    2.請用流程圖的方式告訴我們你是怎麼抓到你的目標資料，流程圖的畫法不拘，主要易懂就好
    3.至少設想並列出 5 種當別人使用你的程式最有可能會遇到的錯誤情況，並提供解決辦法
- 財金指標爬蟲解說
  - 請小組參考"財金指標爬蟲"資料夾中"每組分配到的爬蟲題目.xlsx"，針對分給你們的指標與參考網站，嘗試將該指標的歷史資料爬下來(指標介紹與參考網站在"24 個美國重要經濟指標.docx"中)，時間範圍盡可能從該網站有紀載資料的時間起至程式執行的當下(Now()函數)，將所有的歷史資料都抓下來。並將整理好的資料存在 pandas 的dataframe 中，橫軸為指標數值，標頭為「Value」，縱軸為年-月-日(格式是 Python 的 Datetime ‘yyyy-mm-dd’)，標頭為 Date」，並用 df.head(20)呈現出前 20 筆資料(若用 Jupyter 的人請執行完後再上傳 GitHub，若不是的，結果截圖放在 github 內方便我檢查) 輸出結果請參考圖 2。

## Hw2

- 資料收集與文字探勘共現性進行資料視覺化
  - https://medium.com/ai-society/jkljlj-7d6e699895c4
  2. 針對自訂議題收集相關文本
  3. 將收集到的文本用 NER 挑選出【自定義類別】例如：人名與事件 (可考慮以句子為單位，或是以不同文本來源為彙整文件的基準)。
  4. 將文件與有分類過的單詞進行 TDM (term to matrix)。
  5. 將 TDM 轉成 Co-Occurrence Matrix。
  6. 繪製出各類別之間的共現圖，例如：嫌疑犯和各犯罪行為之間的共現圖。
  7. 每一組都要做一次，以熟悉最基本的 Text Mining 分析流程與手法。

## Hw4

- ETF 評比績效理論實作:
  1. 請用檔案中的三篇論文作為評估 ETF 之指標的實作，評比指標如 A,B,C 三項:
  A. 2009_JBF_Portfolio performance evaluation with generalized Sharpe ratios_ASKSR: 請用第 38 式
  B. 2011_JBF_Omega performance measure and portfolio insurance: 請用第 8 式，L＝無風險利率
  C. 013_EL_A global index of riskiness: 請用 p.494 中之 Q(g)
  2. 請各組根據自己在 HW1 所分配到的 ETF，以及爬蟲程式，將所需的資料從網站(不限來源)扒下來後，用上述 A,B,C 三個評比指標來排列 ETF，用「週資料」及「月資料分析」，程式從 Now()開始回朔至少三年資料，因此最後結果會有兩組 dataframe。