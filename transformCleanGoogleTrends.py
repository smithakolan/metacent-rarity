import pandas as pd


def transformTrends(dapp_df, dapp_name):
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
