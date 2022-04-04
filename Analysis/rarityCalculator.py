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

def getRarity(slug, totalSupply, minRarity, maxRarity):
    nftFile = open('/Users/smithakolan/Documents/GitHub/metacent-rarity/cleanednfts/' + slug +'.json')
    nftData = json.load(nftFile)
    
    rarityList = []
    nftCount = len(nftData)
    for i in range(0, nftCount):
        rarity = 0
        for trait in nftData[i]['traits']:
            if trait['trait_count'] != 0:
                rarity += totalSupply / trait['trait_count']
            
        # Normalize rarity    
        #rarity= (rarity-minRarity)/(maxRarity-minRarity)    
        #print(rarity)           
        nftData[i]['rarity'] = rarity
        rarityList.append(rarity)
    

    nftFile.close()
    rankList = calculateRank(rarityList)
    
    #d = {'rarity':rarityList,'rarity_rank':rankList}
    #df = pd.DataFrame(d, columns=['rarity', 'rarity_rank'])
    #df.to_csv('ranking.csv') 
    for i in range(0, nftCount):
        nftData[i]['rarity_rank'] = rankList[i]
         
        
    return nftData    
    #with open('/Users/smithakolan/Documents/GitHub/metacent-rarity/cleanednfts/' + slug +'.json', 'w') as output:
        #json.dump(nftData, output)
 
        
def calculateRank(vector):
    a={}
    rank=1
    for num in sorted(vector, reverse=True):
      if num not in a:
        a[num]=rank
        rank=rank+1
    return[a[i] for i in vector]


    
def main():
    for index in range(25,50):
        slug = df.loc[index,'slug']
        totalSupply = df.loc[index,'count']
        minRarity = df.loc[index,'minRarity']
        maxRarity = df.loc[index,'maxRarity']
        
        nftData = getRarity(slug, totalSupply, minRarity, maxRarity)
        
        with open('/Users/smithakolan/Documents/GitHub/metacent-rarity/cleanednfts/' + slug +'.json', 'w') as output:
            json.dump(nftData, output)
    
if __name__ == "__main__":
    main()

    
        
