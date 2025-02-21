import time
import random
from datetime import datetime
from kafka import KafkaProducer
import os


# Configuration du producteur Kafka
producer = KafkaProducer(bootstrap_servers="kafka:9092")

# Read the log file
cwd = os.getcwd()
print(cwd)

# Generate a line from the log file
def generate_log():
    x = random.randint(0, len(logs_df.collect()))
    return logs_df[x].value

log_file = "./web_server.log"
f = open(log_file, "r")

# Boucle infinie pour générer les logs
while True:
    for log in f:
        producer.send("log", log.encode("utf-8"))
        print(f"Sent log: {log}")
        time.sleep(random.uniform(0.5, 2.0))  # Envoi des logs avec un délai aléatoire entre 0.5s et 2s

f.close()
