# metacent-rarity

### Basic Setup

The local machine (Linux) requires JAVA, Hadoop and Spark to be installed and configured.

Add environment variables if not have been configured:

```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export SPARK_HOME=/home/{user}/spark-3.1.2-bin-hadoop3.2/
export PYSPARK_PYTHON=python3
```

Start the local ssh :

```bash
sudo service ssh start
```

Start NameNode daemon and DataNode daemon:

```bash
hadoop/hadoop-3.3.1/sbin/start-dfs.sh
```

Clone the project directory:

https://github.com/smithakolan/NFT-Big-Data-Analysis.git

## Data Collection

#### Extraction of Collection Stats

Command to run file: Data_Collection\collect_stats.py

```bash
time ${SPARK_HOME}/bin/spark-submit Data_Collection\collect_stats.py
```

The program produces HDFS folder called DAppStats

<br /> <br />

#### Extraction of NFTs

Command to run file: Data_Collection\getAssets.py

```bash
time ${SPARK_HOME}/bin/spark-submit Data_Collection\getAssets.py
```

The program produces a HDFS folder called nftdata. The file from this folder is acquired.

<br /><br />


#### Extraction of Google Trends

Google Trends is acquired by using a library called PyTrends. It needs to be installed to the project folder before data collection.

```bash
pip install pytrends
```

Command to run file: Data_Collection\getGoogleTrends.py

```bash
python Data_Collection\getGoogleTrends.py
```

The program produces a googleTrends folder. It contains google trends of all dapps.

<br /><br />

#### Extraction of Twitter Account details

Twitter account details is acquired using a library called tweepy. It needs to be installed to the project folder before data collection.

```bash
pip install tweepy
```

Command to run file: Data_Collection\getTwitterDapps.py

```bash
python Data_Collection\getTwitterDapps.py
```

The program produces a JSON file called twitterDapps.

<br /><br />

## Data Cleaning and Integration

#### Transformation, Cleaning and Integration of Dapps

Command to run file: Data_Integration_Cleaning\transformCleanDapps.py

```bash
time ${SPARK_HOME}/bin/spark-submit Data_Integration_Cleaning\transformCleanDapps.py
```

The program produces a JSON file called dapps.json

<br /><br />

#### Transformation, Cleaning and Integration of NFTs

Command to run file: Data_Integration_Cleaning\transformCleanNFT.py

```bash
time ${SPARK_HOME}/bin/spark-submit Data_Integration_Cleaning\transformCleanNFT.py
```

The program produces a HDFS folder called cleanednfts.

<br /><br />

#### Transformation, Cleaning and Integration of Google Trends

Command to run file: Data_Integration_Cleaning\transformCleanGoogleTrends.py

```bash
python Data_Integration_Cleaning\transformCleanGoogleTrends.py
```

The program produces a folder called cleanedGoogleTrends.

<br /><br />

#### Transformation, Cleaning and Integration of Twitter details

Command to run file: Data_Integration_Cleaning\transformCleanTwitterDapps.py

```bash
python Data_Integration_Cleaning\transformCleanTwitterDapps.py
```

The program produces a file called cleanedTwitterDapps.csv

<br /><br />

#### Cleaning and Processing of Dapps

Command to run file: Data_Integration_Cleaning\top10Dapps.py

```bash
python Data_Integration_Cleaning\top10Dapps.py
```

The program produces a file called top_dapps.json

<br /><br />

## Data Loading

#### An AWS account has to be created and a Administrator User account should be created before proceeding to the next step. After creation, the AWS ACCESS_ID and ACCESS_KEY should be added to the following files of the project.

#### Loading of Dapps to Database

Command to run file: Data-Loading\loadDapps.py

```bash
python Data-Loading\loadDapps.py
```

<br /><br />

#### Loading of NFTs to Database

Command to run file: Data-Loading\loadNFT.py

```bash
python Data-Loading\loadNFT.py
```

<br /><br />

#### Rarity calculation

#### Graph Analysis of NFT transactions of each dapp

Graph-Based Analysis of Ethereum Transactions:
Data collection: Made use of SQL quries on FlipSideCrypto application

#### Price prediction of NFTs using Machine Learning
