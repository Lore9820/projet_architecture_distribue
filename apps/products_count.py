from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Initialiser le contexte Spark
spark = SparkSession.builder.appName("AnalyseLogsApacheDF").config("spark.mongodb.output.uri", "mongodb://mongo:27017/logs.products_count").getOrCreate()
sc = spark.sparkContext


# Charger les logs depuis HDFS
log_file = "hdfs://namenode:9000/logs/web_server.log"
logs_df = spark.read.text(log_file)
logs_df = logs_df.selectExpr("CAST(value AS STRING)")


# Parser les logs
parsed_logs = logs_df.withColumn("log_parts", split(col("value"), " ")).select(
        col("log_parts")[0].alias("ip"),  # Adresse IP
        to_timestamp(regexp_extract(col("value"), r'\[(.*?)\]', 1), 'dd/MMM/yyyy:HH:mm:ss Z').alias("timestamp"),  # Extraire la date entre []
        regexp_extract(col("value"), r'"(\w+) ', 1).alias("method"),  # Extraire le verbe HTTP (GET, POST, etc.)
        regexp_extract(col("value"), r'"(?:\w+) (.*?) HTTP', 1).alias("url"),  # Extraire l'URL demandée
        regexp_extract(col("value"), r'HTTP/\d.\d"', 0).alias("protocol"),  # Extraire le protocole HTTP
        col("log_parts")[8].cast("int").alias("status"),  # Code HTTP
        col("log_parts")[9].cast("int").alias("size")  # Taille de la réponse
    )

# Afficher les logs parsés
print(parsed_logs.show(5))

# Produits les plus demandées
top_products = parsed_logs.groupBy('url').count().sort('count', ascending=False)
top_products = top_products.filter(top_products['url'].contains("products"))
top_products = top_products.withColumn("Name", regexp_extract(top_products['url'], r'products/(.*?)\?id', 1))
top_products = top_products.withColumn("ID", regexp_extract(top_products['url'], r'id=(\d+)', 1))
top_products = top_products[['Name', 'ID', 'count']]
print(top_products.show(5))


# Écriture des résultats dans MongoDB
top_products.write.format("mongo").mode("append").option("replaceDocument", "false").save()