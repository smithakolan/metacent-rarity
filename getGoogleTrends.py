import pandas as pd
from pytrends.request import TrendReq


def main():
    pytrends = TrendReq(hl='en-US', tz=360)

    # read dapps.json file and store it as DataFrame
    dapps_df = pd.read_json('dapps.json')

    # traverse through dapps
    for i in range(len(dapps_df)):
        dapp_name = dapps_df.iloc[i]
        dapp_name = dapp_name['name']
        trends = pytrends.get_historical_interest(
            [dapp_name], year_start=2021, month_start=11, day_start=16, year_end=2022, month_end=2, day_end=16, sleep=10)
        trends.to_csv(dapp_name+'.csv')


if __name__ == '__main__':
    main()
