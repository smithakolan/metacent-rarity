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


dappFile = open('/Users/smithakolan/Documents/GitHub/metacent-rarity/dapps.json')
data = json.load(dappFile)

print(len(data))
total_supply = data[0]['stats']['total_supply']

slug = data[0]['slug']



dappFile.close()

nftFile = open('/Users/smithakolan/Documents/GitHub/metacent-rarity/cleanednfts/' + slug +'.json')
data = json.load(nftFile)

nftCount = len(data)

traitCount = len((data[1]['traits']))

rarity = 0
for trait in data[1]['traits']:
    rarity += total_supply / trait['trait_count']
    #print(rarity)
    
data[1]['rarity'] = rarity

print(data[1]) 

#rarity

#for i in count:
    

nftFile.close()