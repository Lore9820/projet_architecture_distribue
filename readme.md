
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

* Access HDFS/namenode container to execute commands :<br>
`docker exec -it projet_architecture_distribue-namenode-1 bash`

* Access Spark container to execute commands :<br>
`docker exec -it spark-master bash`

* Access MongoDB container to execute commands :<br>
`docker exec -it projet_architecture_distribue-mongo-1 mongosh`

### HDFS commands

Commands to put in the Hdfs-namnode terminal once launched with the Windows terminal.

* Create subfolder logs :<br>
`hadoop fs -mkdir /logs`

* Put log file in new subfolder :<br>
`hadoop fs -put web_server.log /logs/web_server.log`

* Exit the HDFS terminal :<br>
`exit`

### Spark commands

Commands to put in the Spark terminal once launched with the Windows terminal.

* Launch the script analyse_logs.py located in the apps subfolder :<br>
`spark-submit --master spark://spark-master:7077 --name AnalyseLogs /opt/spark-apps/analyze_logs.py`

* Launch the script with MongoDB :<br>
`spark-submit --master spark://spark-master:7077 --name AnalyseLogsMongoDB --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 /opt/spark-apps/analyze_logs.py`

### MongoDB commands

Commands to put in the MongoDB terminal once launched with the Windows terminal.

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
` kafka-topics --create --bootstrap-server kafka:9092 --topic log --partitions 1 --replication-factor 1 `

* Checking logs passed through Kafka :<br>
`kafka-console-consumer --bootstrap-server kafka:9092 --topic log --from-beginning`

# Authors

* Lore Goethals
* Clément Tétard