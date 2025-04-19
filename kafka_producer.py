from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

sample_news = [
    {"topic": "politics", "headline": "New policy reforms in healthcare."},
    {"topic": "sports", "headline": "Historic win for Team X in the finals."},
    {"topic": "tech", "headline": "Breakthrough in AI technology revealed."}
]

while True:
    for news in sample_news:
        producer.send(news["topic"], news)
        print(f"Sent: {news}")
        time.sleep(5)

