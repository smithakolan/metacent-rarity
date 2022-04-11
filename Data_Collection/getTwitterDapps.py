#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: swaathi
"""
import tweepy
import json
import pandas as pd


def get_twitter_accounts():
    """
    get_twitter_accounts - retrieve twitter handle names from Dapps
    :return: List of twitter usernames of Dapps
    """
    twitter_username = []
    dapps_df = pd.read_json('dapps.json')

    # traverse through dapps
    for i in range(len(dapps_df)):
        user_name = dapps_df.iloc[i]
        user_name = user_name['twitter_username']
        if(user_name != None):
            twitter_username.append(user_name)
            print(user_name)

    return twitter_username


def get_twitter_data(auth, dapp_twitter_accounts):
    """
    get_twitter_data - retrieve twitter account details from twitter API
    :param auth: auth token
    :param dapp_twitter_accounts: names of the twitter account
    :return: twitter account details of dapps
    """
    api = tweepy.API(auth)
    # getting the users by screen names
    users = api.lookup_users(screen_names=dapp_twitter_accounts)
    return users


def get_dapps_details(twitter_details):
    """
    get_dapps_details - processes the twitter data and stores only the required fields
    :param twitter_details: twitter data of dapps
    :return: stores processed twitter data to json file
    """
    users_obj = []
    for user in twitter_details:
        u_obj = {
            'id': user.id,
            'name': user.name,
            'screen_name': user.screen_name,
            'url': user.url,
            'followers_count': user.followers_count,
            'friends_count': user.friends_count,
            'listed_count': user.listed_count,
            'created_at': str(user.created_at),
            'favourites_count': user.favourites_count,
            'statuses_count': user.statuses_count
        }
        users_obj.append(u_obj)
        with open('twitterDapps.json', 'w') as out:
            json.dump(users_obj, out)


if __name__ == '__main__':

    consumer_key = "xxxxxxxxxxxxxxxxxxxx"
    consumer_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    access_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    access_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    dapp_twitter_accounts = get_twitter_accounts()
    twitter_details = get_twitter_data(auth, dapp_twitter_accounts)
    get_dapps_details(twitter_details)
