from kafka import KafkaProducer
import pandas as pd
import json
import time
import random

df = pd.read_csv('news-article-categories.csv')  
print("Columns in dataset:", df.columns)


allowed_categories = ['politics', 'sports', 'technology']  
filtered_news = [
    {"topic": row['category'].lower(), "headline": row['title']}  
    for _, row in df.iterrows()
    if row['category'].lower() in allowed_categories
]

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)


print(f"Total headlines: {len(filtered_news)}")

while True:
    news = random.choice(filtered_news)
    print(f"Preparing to send: {news}")  
    try:
        producer.send(news["topic"], news)
        print(f"Sent: {news}")  
    except Exception as e:
        print(f"Error sending message: {e}")  
    time.sleep(3) 
