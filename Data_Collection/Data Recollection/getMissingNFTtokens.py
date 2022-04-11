#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: smithakolan
"""
import pandas as pd
import json


def get_asset(asset_contract_address, token_id):
    """
    get_assets - retrieve nfts from Opensea API
    :param asset_contract_address: contract address of the dapp
    :param token_id: token id of the nft
    :return: returns NFT
    """

    url = "https://api.opensea.io/api/v1/asset/" + \
        asset_contract_address+"/" + str(token_id)+"/"

    headers = {"X-API-KEY": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}

    response = requests.request("GET", url, headers=headers)

    if response.status_code != 200:
        if response.status_code == 404:
            print('Not found for {0} '.format(token_id))
        else:
            #raise Exception('API Hit Failed', response)
            print('API Hit Failed', response)
    return response


def main():
    # read dapps.json file and store it as DataFrame
    dapps_df = pd.read_json('dapps.json')

    # traverse through dapps
    for i in range(len(dapps_df)):
        #i = 21
        # dapp_name
        dapp_name = dapps_df.iloc[i]
        dapp_name = dapp_name['slug']
        print(dapp_name)

        # total number of nfts
        total_nfts = dapps_df.iloc[i, 3]
        total_nfts = int(total_nfts['total_supply'])

        cleaned_nfts = pd.read_json(dapp_name+'.json')

        if len(cleaned_nfts) == total_nfts:
            print('No missing NFTs for' + dapp_name)
        else:
            # get token ids of cleaned nfts
            existing_df = cleaned_nfts['token_id']
            existing_df = existing_df.apply(pd.to_numeric)

            # complete list of tokens
            complete_tokens = list(range(1, total_nfts))
            complete_nfts_df = pd.DataFrame(
                complete_tokens, columns=['token_id'])

            # get missing nfts
            missing_df = complete_nfts_df.merge(
                existing_df, how='outer', indicator=True).loc[lambda x: x['_merge'] == 'left_only']
            missing_list = missing_df["token_id"].tolist()

            # store it to file
            with open(dapp_name + '_missing.json', 'w') as out:
                json.dump(missing_list, out)

        break


if __name__ == '__main__':
    main()
