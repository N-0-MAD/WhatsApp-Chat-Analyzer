import pandas as pd
import re
import emoji
import nltk
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


nltk.download('stopwords')

def clean_text(text):
    """
    Preprocesses text by:
    - Lowercasing
    - Removing links, numbers, and special characters
    - Removing stopwords
    - Replacing emojis with text
    """
    text = text.lower()
    text = emoji.demojize(text) 
    text = re.sub(r'@\w+', '@user', text)
    text = re.sub(r'#\w+', '', text)
    text = re.sub(r'http\S+', ' link ', text)
    text = re.sub(r'[^a-zA-Z0-9@#?!,.:\'\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = ' '.join([word for word in text.split() if word not in stopwords.words('english')])
    return text

def perform_topic_modeling(df, num_topics=5):
    """
    Runs LDA topic modeling on WhatsApp chat data.

    Parameters:
        df (pd.DataFrame): Processed chat DataFrame
        num_topics (int): Number of topics to extract

    Returns:
        tuple: (LDA model, vectorizer, transformed data, DataFrame with topics)
    """
    df = df[df['user'] != 'notification']  
    messages = df['message'].dropna().astype(str).tolist()

    cleaned_messages = [clean_text(msg) for msg in messages]

    vectorizer = CountVectorizer(max_features=1000, stop_words='english')
    X = vectorizer.fit_transform(cleaned_messages)

    lda_model = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda_model.fit(X)

    df['topic'] = lda_model.transform(X).argmax(axis=1)

    return lda_model, vectorizer, X, df

def display_topics(model, feature_names, num_words=10):
    """Prints the top words for each topic."""
    for idx, topic in enumerate(model.components_):
        print(f"\n🔹 Topic {idx+1}: ", ", ".join([feature_names[i] for i in topic.argsort()[-num_words:]]))

def plot_topic_trends(df):
    topic_trend = df.groupby(['date', 'topic']).size().unstack(fill_value=0)
    plt.figure(figsize=(12, 6))
    
    for topic in topic_trend.columns:
        plt.plot(topic_trend.index, topic_trend[topic], label=f"Topic {topic}")

    plt.xlabel("Date")
    plt.ylabel("Message Count")
    plt.title("WhatsApp Chat Topic Trends Over Time")
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()

def top_users_per_topic(df):
    """Finds the top 3 users per topic."""
    user_topic_count = df.groupby(['user', 'topic']).size().reset_index(name='count')
    top_users = user_topic_count.sort_values(['topic', 'count'], ascending=[True, False]).groupby('topic').head(3)
    print(top_users)


