import streamlit as st
import pandas as pd
from sqlalchemy import create_engine


st.set_page_config(page_title="News Sentiment Dashboard", layout="wide")


engine = create_engine("mysql+mysqlconnector://root:tanydhelaria123@localhost/news_db")


@st.cache_data
def load_data():
    query = "SELECT * FROM news_articles"
    df = pd.read_sql(query, engine)
    return df


df = load_data()


st.title("News Sentiment Analysis Dashboard")


if df.empty:
    st.warning("No data found in database.")
else:
    # Sidebar for filters
    st.sidebar.header("🔎 Filters")

    # Search by title or content
    search_term = st.sidebar.text_input("Search articles", "")

    # Filter by sentiment
    sentiment_option = st.sidebar.selectbox(
        "Filter by sentiment",
        ("All", "Positive", "Negative", "Neutral")
    )

    # Apply filters
    filtered_df = df.copy()

    if search_term:
        filtered_df = filtered_df[
            filtered_df['title'].str.contains(search_term, case=False) |
            filtered_df['content'].str.contains(search_term, case=False)
        ]

    if sentiment_option == "Positive":
        filtered_df = filtered_df[filtered_df['sentiment_score'] > 0.2]
    elif sentiment_option == "Negative":
        filtered_df = filtered_df[filtered_df['sentiment_score'] < -0.2]
    elif sentiment_option == "Neutral":
        filtered_df = filtered_df[(filtered_df['sentiment_score'] >= -0.2) & (filtered_df['sentiment_score'] <= 0.2)]

    # Sort articles
    sort_by = st.sidebar.selectbox(
        "Sort by",
        ("Newest First", "Oldest First", "Highest Sentiment", "Lowest Sentiment")
    )

    if sort_by == "Newest First":
        filtered_df = filtered_df.sort_values(by="published_time", ascending=False)
    elif sort_by == "Oldest First":
        filtered_df = filtered_df.sort_values(by="published_time", ascending=True)
    elif sort_by == "Highest Sentiment":
        filtered_df = filtered_df.sort_values(by="sentiment_score", ascending=False)
    elif sort_by == "Lowest Sentiment":
        filtered_df = filtered_df.sort_values(by="sentiment_score", ascending=True)

    # Main content
    st.subheader("📋 News Articles")

    if filtered_df.empty:
        st.info("No articles match your filters.")
    else:
        selected_article = st.selectbox(
            "Select an article to view details",
            filtered_df['title']
        )

        # Show article details
        article_data = filtered_df[filtered_df['title'] == selected_article].iloc[0]

        st.markdown(f"### {article_data['title']}")
        st.write(f"🕒 Published: {article_data['published_time']}")
        st.write(f"📈 Sentiment Score: **{article_data['sentiment_score']}**")
        st.write(f"📰 Content:\n\n{article_data['content']}")

    # Sentiment over time
    st.subheader("📈 Sentiment Trend Over Time")
    
    df = df.sort_values(by="published_time")
    st.line_chart(
        data=df,
        x="published_time",
        y="sentiment_score",
        use_container_width=True
    )
