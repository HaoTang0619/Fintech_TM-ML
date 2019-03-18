# Hw1 網路爬蟲


- 需安裝以下已執行全部程式

  ```makefile
  pip install numpy
  pip install selenium
  pip install BeautifulSoup4
  pip install lxml
  pip install pandas
  ```

- 以下範例輸出以 `2019-03-18` 為執行時間

## part 1. ETF 爬蟲

- 檔案名稱：`Crawler.ipynb`

- 從 <https://www.etf.com/> 取得官網後，在官網內能下載每日收盤價的ETF

  - FENY(已下載資料存於`FENY_Price_History_20190315.csv`)
  - TPYP(已下載資料存於`Energy Equity ETF List (80).csv`)

- 無法從其官網取得，或其使用互動是圖表，因為其無法從網頁 source code 內取得，所以使用 <https://finance.yahoo.com/> 作為替代

  - 64 個合法 (2015-12-31 前存在) ETF，請從 `Crawler.ipynb` **cell 2** 的輸出中觀看名單

- 部分內容使用`Selenium.click()`下載 `csv` 檔。已將相關檔案一併附在 hw1 資料夾內，為了方便執行，便將部分下載指令屏蔽，直接開啟本地端檔案。若要實作真實運行狀況，請將相關隱藏程式碼開啟，並從環境變數中將下載路徑改為當前執行資料夾以方便讀檔。

  ![1552922371830](C:\Users\yo930\AppData\Roaming\Typora\typora-user-images\1552922371830.png)

  ![1552922418904](C:\Users\yo930\AppData\Roaming\Typora\typora-user-images\1552922418904.png)

## part 2. 原油庫存指標

- 檔案名稱：`Crawler (ela.gov).ipynb`

- 從 <https://www.eia.gov/petroleum/supply/weekly/> 取得相關資料
- 與 part 1. 相同，已於資料夾內附上相關 `csv` 檔。

![1552921008969](C:\Users\yo930\AppData\Roaming\Typora\typora-user-images\1552921008969.png)