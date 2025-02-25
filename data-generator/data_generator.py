import time
import random
from kafka import KafkaProducer

# Configuration du producteur Kafka
producer = KafkaProducer(bootstrap_servers="kafka:9092")

log_file = "./web_server.log"
f = open(log_file, "r")

# Boucle infinie pour générer les logs
while True:
    for log in f:
        producer.send("log", log.encode("utf-8"))
        print(f"Sent log: {log}")
        time.sleep(random.uniform(0.1, 0.25))  # Envoi des logs avec un délai aléatoire entre 0.5s et 2s

f.close()
