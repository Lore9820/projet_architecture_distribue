#from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import re

# Initialiser le contexte Spark
#sc = SparkContext(appName="AnalyseLogsApacheRDD")
spark = SparkSession.builder.appName("AnalyseLogsApacheDF").getOrCreate()
sc = spark.sparkContext

# Charger les logs depuis HDFS
log_file = "hdfs://namenode:9000/logs/web_server.log"
logs_rdd = sc.textFile(log_file)

# Définir le pattern regex pour parser les logs
log_pattern = r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?) (.*?) HTTP.*" (\d+) (\d+)'

# Fonction pour parser une ligne de log
def parse_log_line(line):
    match = re.match(log_pattern, line)
    if match:
        return (
        match.group(1), # IP
        match.group(2), # Timestamp
        match.group(3), # HTTP Method
        match.group(4), # URL
        int(match.group(5)), # HTTP Status
        int(match.group(6)) # Response Size
        )
    else:
        return None

# Parser les logs
parsed_logs_rdd = logs_rdd.map(parse_log_line).filter(lambda x: x is not None)


# Afficher 10 logs parsés
print("----------------------------------------------------")
print("Exemple de logs parsés :")
for log in parsed_logs_rdd.take(10):
    print(log)
print("----------------------------------------------------")


# Nombre total de requêtes
#total_requests = parsed_logs_rdd.count()
#print("----------------------------------------------------")
#print(f"Nombre total de requêtes : {total_requests}")
#print("----------------------------------------------------")


# Top 5 des produits les plus demandées
top_products = parsed_logs_rdd.map(lambda x: (x[3], 1)).reduceByKey(lambda a, b: a + b)
df_tp = spark.createDataFrame(top_products, ["Product", "Count"])
df_tp = df_tp.filter(df_tp['Product'].contains("products"))
df_tp = df_tp.sort("Count", ascending=False)
df_tp = df_tp.withColumn("Name", F.regexp_extract(df_tp['Product'], r'products/(.*?)id', 1))
df_tp = df_tp.withColumn("ID", F.regexp_extract(df_tp['Product'], r'id=(\d+)', 1))
df_tp = df_tp[['Name', 'ID', 'Count']]
print(df_tp.show(5))


# 




# Nombre de requêtes par méthode HTTP
#nb_requests = parsed_logs_rdd.map(lambda x: (x[2], 1)).reduceByKey(lambda a, b: a + b).takeOrdered(10, key=lambda x: -x[1])
#print("----------------------------------------------------")
#print(f"Nombre de requêtes par methode HTTP :")
#for req, count_req in nb_requests:
#    print(f"{req} : {count_req}")
#print("----------------------------------------------------")


# Taille moyenne des réponses par code HTTP
#avg_resp_size = parsed_logs_rdd.map(lambda x: (x[4], x[5])).reduceByKey(lambda a, b : (a + b)/2 ).collect()
#print("----------------------------------------------------")
#print("Taille moyenne des réponses par code HTTP")
#for code, avg in avg_resp_size:
#    print(f"{code} : {avg}")
#print("----------------------------------------------------")


# IP la plus active
#top_ip = parsed_logs_rdd.map(lambda x: (x[0], 1)).reduceByKey(lambda a, b: a + b).takeOrdered(1, key=lambda x: -x[1])
#print("----------------------------------------------------")
#print("Adresse IP la plus active :")
#for ip, ip_count in top_ip:
#    print(f"{ip}: {ip_count}")
#print("----------------------------------------------------")
