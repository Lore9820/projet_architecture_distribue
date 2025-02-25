from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Initialisation de la session Spark
spark = SparkSession.builder.appName("StreamIpWatch").config("spark.mongodb.output.uri", "mongodb://mongo:27017/logs.streamIpWatch").getOrCreate()

# Lecture des logs depuis Kafka
kafka_df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "kafka:9092").option("subscribe", "log").load()

# Conversion des données en string
logs_df = kafka_df.selectExpr("CAST(value AS STRING)")

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

# Surveillance activité IP
ip_watch = parsed_logs.groupBy(window(col("timestamp"), "2 minutes", "2 minutes"), "ip").count()


# Fonction pour écrire dans MongoDB (sans écraser)
def write_to_mongo(df, epoch_id):
    df_formatted = df.withColumn("start_time", col("window.start")).withColumn("end_time", col("window.end")).drop("window")
    df_formatted.write.format("mongo").mode("complete").option("replaceDocument", "true").save()


# Écriture des résultats dans MongoDB en streaming
query = ip_watch.writeStream.outputMode("complete").foreachBatch(write_to_mongo).start()

query.awaitTermination()
