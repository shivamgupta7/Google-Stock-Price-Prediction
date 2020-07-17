# Google Stock Price Prediction

![Python 3.6](https://img.shields.io/badge/python-3.6.9-orange) ![pip-3](https://img.shields.io/badge/pip-9.0.1-green) ![Python-Kafka 2.0.1](https://img.shields.io/badge/kafka--python-2.0.1-red) ![Pyspark 3.0.0](https://img.shields.io/badge/pyspark-3.0.0-yellowgreen) ![s3fs 0.4.2](https://img.shields.io/badge/s3fs-0.4.2-blue) ![pandas 1.0.5](https://img.shields.io/badge/pandas-1.0.5-green)
![alpha-vantage 2.2.0](https://img.shields.io/badge/alpha--vantage-2.2.0-critical) ![boto3 1.14.16](https://img.shields.io/badge/boto3-1.14.16-ff69b4) ![Flask 1.1.2](https://img.shields.io/badge/Flask-1.1.2-009e73)

![GIF](readme_resources/stock_graph.gif)

Using ALPHA VANTAGE API to predict google stock price.

- Using [ALPHA VANTAGE](https://www.alphavantage.co/) to genrate API Key.

- Using this API key to Download Google Stock Price data for each 1 min interval.

- [Create S3 bucket](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-creating-buckets.html) using boto3. (Boto is the Amazon Web Services (AWS) SDK for Python. It enables Python developers to create, configure, and manage AWS services, such as EC2 and S3. Boto provides an easy to use, object-oriented API, as well as low-level access to AWS services.)

- After creating [bucket upload](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html) **stock data** into bucket using boto3.

-  Reading data from S3 and doing some preprocessing.

- After preprocessing train a Linear Regression model and save model weights.

- Installing [kafka and zookeeper](https://tecadmin.net/install-apache-kafka-ubuntu/) into system and install [python-kafka](https://pypi.org/project/kafka-python/)

- Start zookeeper and kafka server into local system and connect python-kafka to local host.

- **Create a Topic in Kafka**

    Create a topic in kafka using below query. Before create kafka topic you go to kafka folder.
    ```
    $cd /usr/local/kafka/

    $bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic stock_prices
    ```
    The replication-factor describes how many copies of data will be created. As we are running with a single instance keep this value 1.

    Set the partitions options as the number of brokers you want your data to be split between. As we are running with a single broker keep this value 1.

    You can create multiple topics by running the same command as above. After that, you can see the created topics on Kafka by the running below command:

    ```
    bin/kafka-topics.sh --list --zookeeper localhost:2181
    ```

- **Send Messages to Kafka**

    The **producer** is the process responsible for put data into our Kafka. The Kafka comes with a command-line client that will take input from a file or from standard input and send it out as messages to the Kafka cluster. The default Kafka sends each line as a separate message.

    ```
    bin/kafka-console-producer.sh --broker-list localhost:9092 --topic stock_prices
    ```

- **Using Kafka Consumer**

    Kafka also has a command-line consumer to read data from the Kafka cluster and display messages to standard output.

    The first argument is the topic, numtest in our case.
    
    bootstrap_servers=[‘localhost:9092’]: same as our producer

    ```
    bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic stock_prices --from-beginning
    ```
- **Now using python KafkaProducer to connect the local kafka host**

    bootstrap_servers=[‘localhost:9092’]: sets the host and port the producer should contact to bootstrap initial cluster metadata. It is not necessary to set this here, since the default is localhost:9092.

- **Using KafkaConsumer to predict stocks data**

    Using **KafkaConsumer** to get data from producer. After geting data we load save model which save previously when train the model. Using these model we predict close value.

- **Create Flask API**

    In flask I have created 3 URL:

    1. "/" for main page which rander stockgraph.html template for showing predicting close and actual close value.
    2. "/model-train" this URL is use for train model.
    3. "/data" this is for send data to stockgraph.html page for showing graph.

## How To Run

- First start zookeeper and kafka server.
- Run producer file. (``` python3 consumer.py ```)
- Run app file. (``` python3 app.py ```)

![GIF](readme_resources/how_to_run_project_on_localhost.gif)