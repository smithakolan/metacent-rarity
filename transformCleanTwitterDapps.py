import pandas as pd


def get_twitter_accounts(dapps_df):
    twitter_slugs = []
    for i in range(len(dapps_df)):
        dapp = dapps_df.iloc[i]
        row = {
            'slug': dapp['slug'],
            'screen_name': dapp['twitter_username']}
        if(row['screen_name']):
            twitter_slugs.append(row)
    return twitter_slugs


def main():

    twitter_df = pd.read_json('twitterDapps.json')
    twitter_df = twitter_df[['screen_name', 'followers_count']]

    # read dapps.json file
    dapps_df = pd.read_json('dapps.json')
    twitter_slugs = get_twitter_accounts(dapps_df)
    twitter_slugs_df = pd.DataFrame(twitter_slugs)

    twitter_cleaned = pd.merge(
        twitter_df, twitter_slugs_df, on='screen_name', how='inner')
    twitter_cleaned.to_csv('cleanedTwitterDapps.csv')


if __name__ == '__main__':
    main()
