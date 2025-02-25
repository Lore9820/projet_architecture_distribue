
# Projet architecture distribuée

## Informations

Le but du projet est d'analyser un fichier de logs via une architecture distribuée mise en place via Docker.

Les technologies utilisées sont : Docker, Hadoop HDFS, Spark, Kafka, MongoDB.

## Instructions for use

### Windows commands

Commands to put in the Windows terminal opened at the root directory of the project.

* If necessary, build the Hadoop image with the name "hadoop" :<br>
`docker build -t hadoop .`

* Launch the containers :<br>
`docker-compose up -d`

* Verify the containers are running :<br>
`docker ps`

* Put the log file in the namenode :<br>
`docker cp web_server.log projet_architecture_distribue-namenode-1:/`

### HDFS commands

* Access HDFS/namenode container to execute commands :<br>
`docker exec -it projet_architecture_distribue-namenode-1 bash`

* Create subfolder logs :<br>
`hadoop fs -mkdir /logs`

* Put log file in new subfolder :<br>
`hadoop fs -put web_server.log /logs/web_server.log`

* Exit the HDFS terminal :<br>
`exit`

### Spark commands

* Access Spark container to execute commands :<br>
`docker exec -it spark-master bash`

* Launch the script located in the apps subfolder :<br>
`spark-submit --master spark://spark-master:7077 --name AnalyseLogs /opt/spark-apps/analyze_logs.py`

* Launch the script with MongoDB :
    * `spark-submit --master spark://spark-master:7077 --name AnalyseLogsMongoDB --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 /opt/spark-apps/products_count.py`
    * `spark-submit --master spark://spark-master:7077 --name AnalyseLogsMongoDB --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 /opt/spark-apps/status_count.py`
    * `./bin/spark-submit --master spark://spark-master:7077 --name StructuredStreamingKafkaMongoDB --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 /opt/spark-apps/streamErreur.py`
    * `./bin/spark-submit --master spark://spark-master:7077 --name StructuredStreamingKafkaMongoDB --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 /opt/spark-apps/streamIpWatch.py`

### MongoDB commands

* Access MongoDB container to execute commands :<br>
`docker exec -it projet_architecture_distribue-mongo-1 mongosh`

* Show databases :<br>
`show dbs`

* Move in the database logs :<br>
`use logs`

* Show collections :<br>
`show collections`

* Access collections status_count :<br>
`db.status_count.find().pretty()`

### Kafka commands

* Access Kafka container :<br>
`docker exec -it projet_architecture_distribue-kafka-1 /bin/bash`

* Listing all Kafka topics :<br>
`kafka-topics --list --bootstrap-server kafka:9092`

* Creating a topic named log :<br>
`kafka-topics --create --bootstrap-server kafka:9092 --topic log --partitions 1 --replication-factor 1`

* Checking logs passed through Kafka :<br>
`kafka-console-consumer --bootstrap-server kafka:9092 --topic log --from-beginning`

# Authors

* Lore Goethals
* Clément Tétard