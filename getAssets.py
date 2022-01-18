import requests
import time
import pandas as pd


def get_asset(asset_contract_address, token_id):
    headers = {'X-API-KEY ':  '24fba988013a492b8e359d6cb2331e0f '}
    print(asset_contract_address, token_id)
    url = f'https://api.opensea.io/api/v1/asset/{asset_contract_address}/{token_id}/'
    print(url)
    response = requests.request('GET', url, headers=headers)
    print(response.status_code)

    if response.status_code != 200:
        if response.status_code == 404:
            print('Not found for {0} '.format(token_id))
            return None
        else:
            #raise Exception('API Hit Failed', response)
            print('API Hit Failed', response)
    return response


def main():
    # read dapps.json file and store it as DataFrame
    dapps_df = pd.read_json('dapps.json')

    # traverse through dapps
    for i in range(len(dapps_df)):
        #i = 0
        # dapp_name
        dapp_name = dapps_df.iloc[i]
        dapp_name = dapp_name['slug']
        print(dapp_name)
        # contract_address
        asset_contract_address = dapps_df.iloc[i, 1]
        asset_contract_address = asset_contract_address[0]['address']
        # total number of nfts
        total_nfts = dapps_df.iloc[i, 3]
        total_nfts = int(total_nfts['total_supply'])
        assets = []
        #print(asset_contract_address, total_nfts)

        # iterate through total number of nfts and fetch each asset
        for token in range(1, total_nfts+1):
            response = get_asset(asset_contract_address, token)
            print(response)
            if(response):
                assets.append(response)
            if token % 3 == 0:
                time.sleep(10)
                break
        assets = pd.DataFrame(assets)
        # write to file
        # assets.to_json(dapp_name+'.json')
        break


if __name__ == '__main__':
    main()
