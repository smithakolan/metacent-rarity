#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 16:49:06 2022

@author: smithakolan
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import top10Dapps

#Create dataset with individual NFT data
dapps = top10Dapps.top_10_dapps



for dapp in dapps:
    df = pd.read_csv('/Users/smithakolan/Documents/GitHub/metacent-rarity/transaction_data/' + dapp +'.csv', 
                 usecols = ['BLOCK_TIMESTAMP', 'EVENT_FROM','EVENT_TO','PRICE_USD'])
    dfgt=df.dropna()
    dfgt=dfgt.drop_duplicates()
    dfgt.columns = ['Timeset', 'Source', 'Target','Weight']
    dfgt.insert(3, "Type", 'Directed')
    dfgt = dfgt[['Source', 'Target', 'Type', 'Weight', 'Timeset']]
    dfgt = dfgt.sort_values(by=['Timeset'])
    dfgt['Timeset'] = pd.to_datetime(dfgt['Timeset'])
    dfgt['Timeset'] = dfgt['Timeset'].apply(lambda x: x.replace(microsecond=0).isoformat())
    if not os.path.exists('/Users/smithakolan/Documents/GitHub/metacent-rarity/Analysis/processed_transaction_data/'+dapp+'/'):
        os.makedirs('/Users/smithakolan/Documents/GitHub/metacent-rarity/Analysis/processed_transaction_data/'+dapp+'/')
    
    dfgt.to_csv('/Users/smithakolan/Documents/GitHub/metacent-rarity/Analysis/processed_transaction_data/'+dapp+'/links.csv',index = False)
    
    id_list1 = dfgt['Source'].values.tolist()
    id_list2 = dfgt['Target'].values.tolist()
    id_list = id_list1 + id_list2

    listdf = pd.DataFrame(id_list, columns=['Id'])
    listdf = listdf.drop_duplicates()
    listdf.insert(1, 'Name', listdf['Id'])
    listdf.to_csv('/Users/smithakolan/Documents/GitHub/metacent-rarity/Analysis/processed_transaction_data/'+dapp+'/nodes.csv', index = False)






