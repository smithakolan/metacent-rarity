import requests
import time
import pandas as pd
import json


def get_asset(asset_contract_address, token_id):

    url = "https://api.opensea.io/api/v1/asset/" + \
        asset_contract_address+"/" + str(token_id)+"/"

    #headers = {"X-API-KEY": "24fba988013a492b8e359d6cb2331e0f"}
    headers = {"X-API-KEY": "f88ff06861d34122a3d4eb20609fe092"}

    response = requests.request("GET", url, headers=headers)

    # print(url)
    print(response.status_code, token_id)

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
        # specify the location of the dapp in dapps.json
        i = 9

        # dapp_name
        dapp_name = dapps_df.iloc[i]
        dapp_name = dapp_name['slug']
        print(dapp_name)
        missing_df = pd.read_json(dapp_name + '_missing.json')
        # print(missing_df.head())
        # contract_address
        asset_contract_address = dapps_df.iloc[i, 1]
        asset_contract_address = asset_contract_address[0]['address']

        # total number of missing nfts
        missing_list = missing_df[0].tolist()
        total_nfts = len(missing_list)
        assets = []
        count404 = 0
        error_tokens = []
        #print(asset_contract_address, total_nfts)

        # iterate through missing list and fetch each asset
        for j in range(total_nfts):
            token = missing_list[j]
            response = get_asset(asset_contract_address, token)
            if(response and response.status_code == 200):
                assets.append(response.json())

            elif (response.status_code == 404):
                count404 += 1
            elif (response.status_code == 429):
                error_tokens.append(token)

            if count404 != 0 and count404 % 10 == 0:
                print('sleeping')
                time.sleep(60)
                count404 = 0

            if j % 100 == 0 or j == total_nfts-1:
                # write to file
                with open('missing' + dapp_name + str(j)+'.json', 'w') as out:
                    json.dump(assets, out)
                with open('error' + dapp_name + str(j)+'.json', 'w') as out:
                    json.dump(error_tokens, out)
                assets = []
                error_tokens = []

            if j % 20 == 0:
                time.sleep(10)

        break


if __name__ == '__main__':
    main()
