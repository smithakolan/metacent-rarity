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


def create_dapps_table():
    """
    create_dapp_table - creates dapps table in Dyanmo DB
    :return: table status
    """
    table = dynamodb.create_table(
        TableName='Dapps',
        KeySchema=[
            {
                'AttributeName': 'slug',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'slug',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


def insert_into_table(dapps):
    """
    insert_into_table - inserts data into stats table
    :param dapps: dapps data
    """
    selected_dapps = dapps
    table = dynamodb.Table('Dapps')
    i = 0
    for dapp in selected_dapps:
        table.put_item(Item=dapp)
        print(dapp['slug'], i)
        i += 1

    # to avoid write throttle
    # time.sleep(1)


if __name__ == '__main__':

    # Create Table
    dapp_table = create_dapps_table()

    # to wait for the table to get created
    time.sleep(60)

    # read json file
    with open("./top_dapps.json") as json_file:
        dapp_list = json.load(json_file, parse_float=Decimal)

    # insert into table
    insert_into_table(dapp_list)
