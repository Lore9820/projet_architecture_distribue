
# Projet architecture distribuée

## Informations

Le but du projet est d'analyser un fichier de logs via une architecture distribuée mise en place via Docker.

Les technologies utilisées sont : Docker, Hadoop HDFS, Hadoop Spark, MongoDB.

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

# Authors

* Lore Goethals
* Clément Tétard