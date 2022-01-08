import requests
import time
import json
import collections_dapps as cdapps
from pyspark.sql import SparkSession, functions, types
import sys
assert sys.version_info >= (3, 5)  # make sure we have Python 3.5+


def get_dapps(slug_name, offset):
    headers = {'X-API-KEY ':  '24fba988013a492b8e359d6cb2331e0f '}
    print('slugname, offset', slug_name, offset)
    url = f'https://api.opensea.io/api/v1/assets?order_by=sale_count&order_direction=desc&offset={offset}&limit=50&collection={slug_name}'
    print(url)
    response = requests.request('GET', url, headers=headers)
    print(response.status_code)

    if response.status_code != 200:
        if response.status_code == 404:
            print('Not found for {0} '.format(slug_name))
            return None
        else:
            #raise Exception('API Hit Failed', response)
            print('API Hit Failed', response)
    return response


def main():
    collectionsFile = open('slug_coll.txt', 'r')
    Collections = collectionsFile.readlines()
    for collection in Collections:
        int i = 0
        
    slug_names_list = cdapps.collection_slug_names
    print(slug_names_list)
    response_list = []
    slug_name = 'cryptopunks'
    # call api for every slug name on the list
    #for slug_name in slug_names_list[25:29]:
    i = 0
    response = get_dapps(slug_name, 0)
            
    data = response.json()
    if(data['assets'] and len(data['assets']) > 0):
        response_list.append(data['assets'])
        print(len(data['assets']))
        json_rdd = sc.parallelize(data['assets'])
        json_rdd.map(json.dumps).saveAsTextFile(slug_name)

        #i = i+28

    # flatten response_list
    # nfts = []
    # for sublist in response_list:
    #     for item in sublist:
    #         nfts.append(item)

    #print('NFTs :', nfts)

    # json_rdd = sc.parallelize(nfts)
    # json_rdd.map(json.dumps).saveAsTextFile('nft1')


if __name__ == '__main__':
    spark = SparkSession.builder.appName('Get NFTs').getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main()
