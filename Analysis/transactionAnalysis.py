#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 21:29:48 2022

@author: smithakolan
"""

import matplotlib.pyplot as plt
import networkx as nx

G = nx.MultiDiGraph()

G.add_edge(0,1,color='r',weight=1)
G.add_edge(1,2,color='g',weight=0.004)
G.add_edge(2,3,color='b',weight=0.00003)
G.add_edge(3,4,color='y',weight=0.008)
G.add_edge(4,0,color='m',weight=0.006)

colors = nx.get_edge_attributes(G,'color').values()
weights = nx.get_edge_attributes(G,'weight').values()

pos = nx.circular_layout(G)
nx.draw(G, pos, 
        arrowstyle = 'fancy',
        connectionstyle="arc3,rad=0.05",
        edge_color=colors, 
        width=list(weights),
        with_labels=True,
        node_color='lightgreen')

ax = plt.gca()
ax.margins(0.08)
plt.axis("off")
plt.tight_layout()
plt.show()

