#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 12:45:35 2022

@author: smithakolan
"""
# Imports
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from fa2 import ForceAtlas2
from curved_edges import curved_edges
import pandas as pd
import numpy as np

df = pd.read_csv("/Users/smithakolan/Documents/GitHub/metacent-rarity/transaction_data/alienfrensnft.csv", usecols = ['EVENT_FROM','EVENT_TO','PRICE_USD'])
#dfgt = pd.DataFrame(df, columns =['source', 'target','weight'])
#print(df)
dfgt=df.dropna()
dfgt.columns = ['source', 'target','weight']
#print(df2)
#dfgt = pd.DataFrame(df2, columns =['source', 'target','weight'])
#print(dfgt)

G = nx.from_pandas_edgelist(dfgt, source='source', target='target', edge_attr='weight')
forceatlas2 = ForceAtlas2(edgeWeightInfluence=0)
positions = forceatlas2.forceatlas2_networkx_layout(G, pos=None, iterations=1000)

# Get curves
curves = curved_edges(G, positions)

# Make a matplotlib LineCollection - styled as you wish
weights = np.array([x[2]['weight'] for x in G.edges(data=True)])
widths = 0.5 * np.log(weights)
lc = LineCollection(curves, color='w', alpha=0.25, linewidths=widths)

# Plot
plt.figure(figsize=(10,10))
plt.gca().set_facecolor('k')
nx.draw_networkx_nodes(G, positions, node_size=10, node_color='w', alpha=0.5)
plt.gca().add_collection(lc)
plt.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False)
plt.show()
plt.savefig("graph.pdf")
