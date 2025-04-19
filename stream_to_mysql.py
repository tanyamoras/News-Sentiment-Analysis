from kafka import KafkaConsumer
import json
import mysql.connector
from textblob import TextBlob

consumer = KafkaConsumer(
    'politics', 'sports', 'tech',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root1234',
    database='news_db'
)

cursor = conn.cursor()

for msg in consumer:
    headline = msg.value['headline']
    sentiment = "positive" if TextBlob(headline).sentiment.polarity > 0 else "negative"
    cursor.execute("INSERT INTO sentiment_analysis (headline, sentiment) VALUES (%s, %s)", (headline, sentiment))
    conn.commit()
    print(f"Inserted: {headline} → {sentiment}")

