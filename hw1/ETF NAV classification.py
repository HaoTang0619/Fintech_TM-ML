
# coding: utf-8

# In[1]:


#依公司分類ETF

Class = { "Alerian": ['ENFR', 'AMLP'], "Barclays": ['ATMP'], "Suisse": ['MLPO'], 
         "Direxion": ['ERY', 'ERX', 'GASX', 'GASL', 'DRIP', 'GUSH', 'ZMLP'], "SPDR": ['XLE', 'XES', 'XOP'],
         "ETRACS": ['AMU', 'AMUB', 'MLPB'], "Fidelity": ['FENY'],
         "FirstTrust": ['FXN', 'FAN', 'FCG', 'QCLN', 'GRID', 'EMLP'], "Global": ['GREK', 'MLPX', 'MLPA', 'CHIE', 'YLCO'],
         "Infra": ['AMZA'], "Invesco": ['ENY', 'PZD', 'PXI', 'PXE', 'PXJ', 'PBD', 'RYE', 'PSCE', 'TAN', 'PBW', 'PUW'],
         "iPath": ['IMLP'], "iShares": ['ICLN', 'IXC', 'FILL', 'IYE', 'IEO', 'IEZ'], "JP": ['AMJ'], "Miller": ['MLPC'],
         "Morgan": ['MLPY'], "ProShares": ['DIG', 'DUG', 'DDG'], "Tortoise": ['TPYP'], "UBS": ['MLPI', 'MLPG'],
         "VanEck": ['KOL', 'GEX', 'YMLI', 'YMLP', 'CRAK', 'OIH', 'FRAK', 'NLR'], "Vanguard": ['VDE'] }


# In[7]:


#依公司、爬蟲來源分類

ETFcom = { "Invesco": ['PZD', 'PXI', 'PXE', 'PXJ', 'PBD', 'RYE', 'PSCE', 'TAN', 'PBW'], 
          "SPDR": ['XLE'], "ProShares": ['DIG', 'DUG', 'DDG'], "Tortoise": ['TPYP'], 
          "VanEck": ['KOL', 'GEX', 'YMLI', 'YMLP', 'CRAK', 'OIH', 'FRAK', 'NLR'],
         "iShares": ['ICLN', 'IXC', 'FILL', 'IYE', 'IEO', 'IEZ'],
         } 

YahooFin = { "Morgan": ['MLPY'], "Infra": ['AMZA'], "Alerian": ['ENFR', 'AMLP'], "Barclays": ['ATMP'],
           "Direxion": ['ERY', 'ERX', 'GASX', 'GASL', 'DRIP', 'GUSH', 'ZMLP'], "ETRACS": ['AMU', 'AMUB', 'MLPB'],
           "Suisse": ['MLPO'], "Fidelity": ['FENY'], "FirstTrust": ['FXN', 'FAN', 'FCG', 'QCLN', 'GRID', 'EMLP'],
           "iPath": ['IMLP'], "JP": ['AMJ'], "Miller": ['MLPC'], "UBS": ['MLPI', 'MLPG'],"Vanguard": ['VDE'],
           "Global": ['GREK', 'MLPX', 'MLPA', 'CHIE', 'YLCO'], "SPDR": ['XES', 'XOP'], "Invesco": ['ENY','PUW'] 
           }


# In[13]:


#list
#要從Yahoo finance爬的ETF (總共38個要從Finance找)
YahooFinance = ['MLPY', 'AMZA', 'ENFR', 'AMLP', 'ATMP', 'ERY', 'ERX', 'GASX', 'GASL', 'DRIP', 'GUSH', 'ZMLP',
               'AMU', 'AMUB', 'MLPB', 'MLPO', 'FENY', 'FXN', 'FAN', 'FCG', 'QCLN', 'GRID', 'EMLP', 'IMLP', 'AMJ', 'MLPC',
               'MLPI', 'MLPG', 'VDE', 'GREK', 'MLPX', 'MLPA', 'CHIE', 'YLCO', 'ENY', 'XES', 'XOP' , 'PUW']

#要從ETF.com爬的ETF
ETFCom = ['PZD', 'PXI', 'PXE', 'PXJ', 'PBD', 'RYE', 'PSCE', 'TAN', 'PBW', 'XLE', 'DIG', 'DUG', 'DDG', 'TPYP', 
          'KOL', 'GEX', 'YMLI', 'YMLP', 'CRAK', 'OIH', 'FRAK', 'NLR', 'ICLN', 'IXC', 'FILL', 'IYE', 'IEO', 'IEZ']

