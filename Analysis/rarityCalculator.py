#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 13:55:06 2022

@author: smithakolan
"""



#import getDataFromDB as getNFT
import json
import pandas as pd

filename = 'rarityRanges.csv'
df = pd.read_csv(filename)

#print(len(df.index))
print(df.loc[0,'slug'])

def getRarity(slug, totalSupply, minRarity, maxRarity):
    nftFile = open('/Users/smithakolan/Documents/GitHub/metacent-rarity/cleanednfts/' + slug +'.json')
    nftData = json.load(nftFile)
    
    nftCount = len(nftData)
    for i in range(0, nftCount):
        rarity = 0
        for trait in nftData[i]['traits']:
            rarity += totalSupply / trait['trait_count']
            
        rarity= (rarity-minRarity)/(maxRarity-minRarity)    
        #print(rarity)           
        nftData[i]['rarity'] = rarity
    
    nftFile.close()
    with open('/Users/smithakolan/Documents/GitHub/metacent-rarity/cleanednfts/' + slug +'.json', 'w') as output:
        json.dump(nftData, output)

for index in range(0,1):
    slug = df.loc[index,'slug']
    totalSupply = df.loc[index,'count']
    minRarity = df.loc[index,'minRarity']
    maxRarity = df.loc[index,'maxRarity']
    
    getRarity(slug, totalSupply, minRarity, maxRarity)
    
    
        
