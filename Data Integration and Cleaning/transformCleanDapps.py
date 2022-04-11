import json
from pyspark.sql import SparkSession
import sys
assert sys.version_info >= (3, 5)  # make sure we have Python 3.5+


def get_selective_fields(dapps_obj):
    del dapps_obj['collection']['editors']
    return dapps_obj['collection']


def main():
    dapps_text = sc.textFile("DAppStats/part*")
    dapps_json = dapps_text.map(lambda line: json.loads(line))
    dapps_selected = dapps_json.map(get_selective_fields)

    jsonRDD = dapps_selected.map(json.dumps)
    json_string = jsonRDD.reduce(lambda x, y: x + ",\n" + y)

    # writing to a local file
    with open("dapps.json", "wb") as f:
        f.write(json_string.encode("utf-8"))


if __name__ == '__main__':
    spark = SparkSession.builder.appName(
        "Transform and Clean Dapps").getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main()
