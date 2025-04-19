import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root1234',
    database='news_db'
)

query = "SELECT sentiment, COUNT(*) as count FROM sentiment_analysis GROUP BY sentiment"
df = pd.read_sql(query, conn)

# Plot
df.plot(kind='bar', x='sentiment', y='count', title='Sentiment Distribution (Batch)')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('batch_sentiment_distribution.png')
plt.show()

