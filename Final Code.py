#!/usr/bin/env python
# coding: utf-8

# In[11]:


import requests
import os
from dotenv import load_dotenv
import pandas as pd


# In[12]:


env_file = 'env_vars_dgroner_ws.env'
load_dotenv(env_file)
myAPIKey = os.getenv('ALPHAVANTAGE_KEY')
print(myAPIKey)


# In[18]:


symbols = ['XLE', 'XLB', 'XLI', 'XLY', 'XLP', 'XLV', 'XLF', 'XLK', 'XLC', 'XLU', 'XLRE', '^GSPC']
API_URL = "https://www.alphavantage.co/query"

def GetData(symbol, myAPIKEY, API_URL):
    data = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "interval": "Daily",
        "datatype": "json",
        "apikey": myAPIKey
             }
    resultList = []
    response = requests.get(API_URL,  data)
    data = response.json()
    data = data['Time Series (Daily)']
    return data


# In[21]:


data_XLE = GetData("XLE", myAPIKey, API_URL)
data_XLB = GetData("XLB", myAPIKey, API_URL)
data_XLI = GetData("XLI", myAPIKey, API_URL)
data_XLY = GetData("XLY", myAPIKey, API_URL)


# In[22]:


data_XLP = GetData("XLP", myAPIKey, API_URL)
data_XLV = GetData("XLV", myAPIKey, API_URL)
data_XLF = GetData("XLF", myAPIKey, API_URL)
data_XLK = GetData("XLK", myAPIKey, API_URL)


# In[23]:


data_XLC = GetData("XLC", myAPIKey, API_URL)
data_XLU = GetData("XLU", myAPIKey, API_URL)
data_XLRE = GetData("XLRE", myAPIKey, API_URL)
data_SP500 = GetData("^GSPC", myAPIKey, API_URL)

DataList = [data_XLE,data_XLB,data_XLI,data_XLY,data_XLP,data_XLV,data_XLF,data_XLK,data_XLC,data_XLU,data_XLRE,data_SP500]
myDict = dict(zip(symbols, DataList))


# In[24]:


# consolidate the data into a pandas dataframe
# reset index to datetime

def ConsolidateData(data):
    # consolidate the data into a dataframe
    df = pd.DataFrame(data).transpose()
    # reset the index to Datetime
    df.index = pd.to_datetime(df.index)
    # name index column
    df.index.name = "Date"
    # convert str to numeric
    df["4. close"] = df["4. close"].astype("float")
    return df

df_list = []
for key in myDict:
    df_key = ConsolidateData(myDict[key])
    df_list.append(df_key)
    
df_dict = dict(zip(symbols,df_list))
df_SP500 = df_dict.popitem()
df_SP500


# In[25]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches

for key in df_dict:
    plt.figure(figsize=(16,10)) 

    # ax1 is the twin axis of ax0
    ax0 = plt.subplot(221)
    ax1 = ax0.twinx()   # twinx to share y

    ax0.plot("4. close", data=df_dict[key], c='b')
    ax1.plot("4. close", data=df_SP500[1], c='g')

    # set date title
    plt.title(key + " vs SP500 Closing Data")

    # customize legend
    key = mpatches.Patch(color='blue', label="XLE")
    SP500 = mpatches.Patch(color='green', label='S&P500')
    plt.legend(handles=[key, SP500])


# In[26]:


# calculate daily return data for each sector and the S&P500
SP500_return = df_SP500[1]["4. close"].pct_change()[1:]

def Scatter(return_data):
    return(plt.scatter(SP500_return, return_data))

for key in df_dict:
    key_return = df_dict[key]["4. close"].pct_change()[1:]
    fig = plt.figure()
    plt.scatter(SP500_return, key_return)
    plt.title("S&P500 VS " + key)
    plt.xlabel("S&P500")
    plt.ylabel(key)
    plt.show


# In[27]:


# calculate correlation between sector and S&P500 daily returns 
import statsmodels.api as sm

def correlation(return_data):
    # regression of sector vs S&P500
    indvars = sm.add_constant(SP500_return)
    model = sm.OLS(return_data, indvars).fit()
    summary = model.summary()
    print(summary)

for key in df_dict:
    print(key)
    key_return = df_dict[key]["4. close"].pct_change()[1:]
    print(correlation(key_return))


# In[ ]:




