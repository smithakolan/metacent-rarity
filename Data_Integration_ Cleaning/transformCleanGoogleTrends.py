#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: swaathi
"""

import pandas as pd


def transformTrends(dapp_df, dapp_name):
    """
    transformTrends - transforms hour-wise search data to day-wise data
    :param dapp_df: Google trends for dapps dataframe
    :param dapp_name: slug name of dapps
    :return: returns a new dapp dataframe with processed day-wise search counts
    """
    dapp_df['date'] = pd.to_datetime(dapp_df['date']).dt.date
    dapp_df = dapp_df.groupby(
        'date')[dapp_name].sum().reset_index(name='search_count')
    return dapp_df


def main():
    # read dapps.json file
    dapps_df = pd.read_json('dapps.json')

    for i in range(len(dapps_df)):
        dapp = dapps_df.iloc[i]
        dapp_name = dapp['name']
        slug = dapp['slug']
        dapp_df = pd.read_csv('googleTrends/'+dapp_name+'.csv')
        dapp_df = transformTrends(dapp_df, dapp_name)
        dapp_df.to_csv('cleanedGoogleTrends/'+slug+'Trends.csv')


if __name__ == '__main__':
    main()
