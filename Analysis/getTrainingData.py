#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 21:59:06 2022

@author: smithakolan
"""

import shap
import top10Dapps
import json
import pandas as pd

#Get NFT ID, RARITY, LAST SALE PRICE, NO. OF TRANSACTIONS
dapps = top10Dapps.top_10_dapps

for dapp in dapps:
    nftFile = open('/Users/smithakolan/Documents/GitHub/metacent-rarity/cleanednfts/' + dapp +'.json')
    nftData = json.load(nftFile)

    tnxsdf = pd.read_csv('/Users/smithakolan/Documents/GitHub/metacent-rarity/transaction_data/'+ dapp+ '.csv',
                             usecols = ['TOKEN_ID'])

    tnxsCount = tnxsdf.groupby(['TOKEN_ID']).size().reset_index(name='counts')

    dataList = []
    nftCount = len(nftData)
    for i in range(0, nftCount):
        token_id = nftData[i]['token_id']
        rarity = nftData[i]['rarity']
    
        if(nftData[i]['last_sale']):
            last_sale_price = nftData[i]['last_sale']['total_price']
        
        else:
            last_sale_price = None
    
        dataList.append([token_id, rarity, last_sale_price])
    
    df = pd.DataFrame(dataList, columns =['TOKEN_ID', 'rarity', 'last_sale_price'])
    df['TOKEN_ID'] = pd.to_numeric(df['TOKEN_ID'])

    newDF = pd.merge(df, tnxsCount, on='TOKEN_ID', how='outer')

    newDF = newDF.dropna()


    newDF.to_csv('/Users/smithakolan/Documents/GitHub/metacent-rarity/training_data/' + dapp + '.csv', index = False)

    
"""

dataList
    

# load JS visualization code to notebook
shap.initjs()

# use Tree SHAP explainer to explain the gradient boosting tree model
# you only need to explain and plot the first explaination
# --- Write your code below ---

explainer = shap.TreeExplainer(gb)
shap_values = explainer.shap_values(X_test)

# visualize the first prediction's explanation (use matplotlib=True to avoid Javascript)
display(shap.force_plot(explainer.expected_value, shap_values[0,:], X_test.iloc[0,:]))

# shap.force_plot(explainer.expected_value, shap_values[0,:], X_test.iloc[0,:], link="logit")
shap.summary_plot(shap_values, features=X_test, feature_names=feature_names)

# Rarity, Last Sale price, 
"""
