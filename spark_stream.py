
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType
from textblob import TextBlob
import json

# UDF for Sentiment Analysis
def analyze_sentiment(text):
    blob = TextBlob(text)
    return "positive" if blob.sentiment.polarity > 0 else "negative"

sentiment_udf = udf(analyze_sentiment, StringType())

# Spark session
spark = SparkSession.builder \
    .appName("NewsSentimentStreaming") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Read Kafka stream
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "politics,sports,tech") \
    .load()

# Convert Kafka value to JSON string
df_parsed = df.selectExpr("CAST(value AS STRING) as json_str")

# Extract headline from JSON
@udf(StringType())
def get_headline(json_str):
    try:
        return json.loads(json_str)["headline"]
    except:
        return ""

df_cleaned = df_parsed.withColumn("headline", get_headline(col("json_str")))
df_cleaned = df_cleaned.withColumn("sentiment", sentiment_udf(col("headline")))

# Write to console for demo
query = df_cleaned.select("headline", "sentiment") \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()

