#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: swaathi
"""
import slug_names as cdapps
import json
import pandas as pd
from pyspark.sql import SparkSession
import sys
assert sys.version_info >= (3, 5)  # make sure we have Python 3.5+


def get_selective_fields(nft_object, dapp_name):
    """
    get_selective_fields - retrieves required fields from a nft object

    :param nft_object: single nft object
    :return: returns a new nft object with only required fields
    """
    if(nft_object != None):
        last_sale = {}
        creator = {}
        orders = []
        traits = []
        owner = {}
        # to check if there are traits and select fields
        if nft_object['traits']:
            for obj in nft_object['traits']:
                if isinstance(obj, list):
                    trait = {
                        "trait_type": obj[4],
                        "value": obj[5],
                        "trait_count": obj[3]
                    }
                    traits.append(trait)
                else:
                    trait = {
                        "trait_type": obj['trait_type'],
                        "value": obj['value'],
                        "trait_count": obj['trait_count']
                    }
                    traits.append(trait)

        # last sale selection
        if nft_object['last_sale']:
            total_price = nft_object['last_sale']['total_price']
            decimal = nft_object['last_sale']['payment_token']['decimals']
            total_price = float(total_price) / float(pow(10, decimal))
            last_sale = {
                'payment_token_symbol': nft_object['last_sale']['payment_token']['symbol'],
                'event_type': nft_object['last_sale']['event_type'],
                'event_timestamp': nft_object['last_sale']['event_timestamp'],
                'auction_type': nft_object['last_sale']['auction_type'],
                'total_price': total_price
            }

        # creator selection
        if nft_object['creator']:
            username = ''
            if nft_object['creator']['user']:
                username = nft_object['creator']['user']['username']
            creator = {
                'username': username,
                'profile_img_url': nft_object['creator']['profile_img_url'],
                'address': nft_object['creator']['address']
            }

        # orders selection
        if nft_object['orders']:
            for obj in nft_object['orders']:
                base_price = obj['base_price']
                decimal = obj['payment_token_contract']['decimals']
                base_price = float(base_price) / float(pow(10, decimal))
                order = {
                    'payment_token_symbol': obj['payment_token_contract']['symbol'],
                    'created_date': obj['created_date'],
                    'closing_date': obj['closing_date'],
                    'expiration_time': obj['expiration_time'],
                    'listing_time': obj['listing_time'],
                    'quantity': obj['quantity'],
                    'base_price': base_price
                }
                orders.append(order)

        # owner selection
        if nft_object['owner']:
            owner = {
                'user': nft_object['owner']['user'],
                'profile_img_url': nft_object['owner']['profile_img_url'],
                'address': nft_object['owner']['address']
            }
        # constructing new nft object
        new_nft_object = {
            'id': nft_object['id'],
            'token_id': nft_object['token_id'],
            'num_sales': nft_object['num_sales'],
            'background_color': nft_object['background_color'],
            'nft_name': nft_object['name'],
            'nft_description': nft_object['description'],
            'image_url': nft_object['image_url'],
            'image_preview_url': nft_object['image_preview_url'],
            'image_thumbnail_url': nft_object['image_thumbnail_url'],
            'image_original_url': nft_object['image_original_url'],
            'animation_url': nft_object['animation_url'],
            'animation_original_url': nft_object['animation_original_url'],
            'external_link': nft_object['external_link'],
            'permalink': nft_object['permalink'],
            'token_metadata': nft_object['token_metadata'],
            'owner': owner,
            'sell_orders': nft_object['sell_orders'],
            'creator': creator,
            'top_bid': nft_object['top_bid'],
            'listing_date': nft_object['listing_date'],
            'is_presale': nft_object['is_presale'],
            'orders': orders,
            'auctions': nft_object['auctions'],
            'top_ownerships': nft_object['top_ownerships'],
            'ownership': nft_object['ownership'],
            'slug': dapp_name,
            'traits': traits,
            'last_sale': last_sale


        }
        return new_nft_object


def main():
    # retrieve data for every dapp collection
    for i in range(len(cdapps.collection_slug_names)):

        dapp_name = cdapps.collection_slug_names[i]
        nft_json = spark.read.json("nftdata/"+dapp_name+"*")
        # selecting required json fields for use cases
        nft_selected = nft_json.rdd.map(
            lambda nft: get_selective_fields(nft, dapp_name))

        jsonRDD = nft_selected.map(json.dumps)
        json_string = jsonRDD.reduce(lambda x, y: x + ",\n" + y)
        json_string = '[' + json_string+']'
        # writing to a local file
        with open("cleanednfts/"+dapp_name+".json", "wb") as f:
            f.write(json_string.encode("utf-8"))


if __name__ == '__main__':
    spark = SparkSession.builder.appName(
        "Transform & Clean NFTs").getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main()
