#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 13:55:06 2022

@author: smithakolan
"""

"""
1. Calculating rarity for each NFT
2. Create a new pandas dataframe for each Dapp which contains ['id','token_id', 'nft_name', 'image_url', 'slug', 'last_sale_total_price', 'rarity']
3. Rarity is calculated by looking at count of attributes as well as the number of sales of the NFT & last_sale_total_price
4. At the end, a csv is created for each Dapp.
"""

#import getDataFromDB as getNFT
import json
import pandas as pd
import numpy as np


dappFile = open('/Users/smithakolan/Documents/GitHub/metacent-rarity/dapps.json')
dappData = json.load(dappFile)

print(len(dappData))
rarityRanges = []
for i in range(0,len(dappData)):
    slug = dappData[i]['slug']
    nftCount = dappData[i]['stats']['count']
    
    traitCount = []
    minRarity = 0
    maxRarity = 0
    for traitType in dappData[i]['traits']:
        for iTrait in dappData[i]['traits'][traitType]:
            traitCount.append(dappData[i]['traits'][traitType][iTrait])
        traitCount.sort()
        #print(traitCount)
        if traitCount[0] != 0 :
            maxRarity += nftCount/traitCount[0]
        if traitCount[-1] != 0:
            minRarity += nftCount/traitCount[-1]
        traitCount = []
    rarityRanges.append([slug, nftCount, minRarity, maxRarity])
    traitCount = []
    minRarity = 0
    maxRarity = 0
    
print(rarityRanges)    


dappFile.close()

np.savetxt("rarityRanges.csv", 
           rarityRanges,
           delimiter =", ", 
           fmt ='% s')
