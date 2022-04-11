#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 13:45:26 2022

@author: smithakolan
"""

import json
import pandas as pd
import numpy as np


dappFile = open('/Users/smithakolan/Documents/GitHub/metacent-rarity/dapps.json')
dappData = json.load(dappFile)

print(dappData[0]['primary_asset_contracts'][0]['address'])

print(len(dappData))
addressList = []
for i in range(0,len(dappData)):
    slug = dappData[i]['slug']
    address = dappData[i]['primary_asset_contracts'][0]['address']
    
    addressList.append([slug, address])

print(addressList)    


dappFile.close()

np.savetxt("contractAddresses.csv", 
           addressList,
           delimiter =", ", 
           fmt ='% s')
