from selenium import webdriver
import time
import os
import pandas as pd
import datetime

file = "psw01.xls"

# Determine if the file exists to avoid repeated downloads.

if os.path.isfile(file) == False:
    # Determine download directory.
    
    here = os.getcwd()
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": here}
    options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome("chromedriver.exe",chrome_options=options)
    url = "https://www.eia.gov/petroleum/supply/weekly/"
    driver.get(url)
    xls = driver.find_element_by_link_text("XLS").click()
    time.sleep(12)
    driver.quit()

# Data processing.

data = pd.read_excel(file,sheet_name = None)
table = data.get("Data 1")
cols = table.columns
tmp = table.loc[:,cols[0]].tolist()

# Set the form of "Date" to "yyyy-mm-dd".

for i in range(2,len(tmp)):
    tmp[i] = "{:%Y-%m-%d}".format(tmp[i])
table.loc[:,cols[0]] = pd.Series(tmp)

# Set columns' name and create the frame.

table.rename(columns = {cols[0] : "Date",cols[2] : "Value"},inplace = True)
table.set_index("Date", inplace=True)
t = table.Value[2:]
t = t.to_frame()
t.reset_index("Date", inplace=True)
t