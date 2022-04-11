#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: swaathi
"""
import boto3
import json
from decimal import Decimal
import time


AWS_ACCESS_KEY_ID = 'xxxxxxxxxxxxxxxxxxxx'
AWS_SECRET_ACCESS_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxx'

aws_db_url = 'https://dynamodb.us-west-2.amazonaws.com'
dynamodb = boto3.resource(
    'dynamodb', aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name='us-west-2', endpoint_url=aws_db_url)

# Local DynamoDB for testing
# local_db_url = 'http://localhost:8000'
# dynamodb = boto3.resource(
#     'dynamodb', region_name='us-west-2', endpoint_url=local_db_url)


def create_nft_table():
    """
    create_nft_table - creates nfts table in Dyanmo DB
    :return: table status
    """
    table = dynamodb.create_table(
        TableName='NFTs',
        KeySchema=[
            {
                'AttributeName': 'slug',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'rarity_rank',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'rarity_rank',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'slug',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 20
        }
    )
    return table


def insert_into_table(nfts):
    """
    insert_into_table - inserts data into nfts table
    :param nfts: nfts data
    """
    new_nfts = nfts
    table = dynamodb.Table('NFTs')
    i = 0
    for nft in new_nfts:
        table.put_item(Item=nft)
        i += 1

    # to avoid write throttle
    # time.sleep(1)


if __name__ == '__main__':

    # Create Table
    nft_table = create_nft_table()
    # to wait for the table to get created
    time.sleep(60)

    # coolcats added
    # read json file
    with open("./cleanednfts/meebits.json") as json_file:
        nft_list = json.load(json_file, parse_float=Decimal)

    # insert into table
    insert_into_table(nft_list)
