import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from datetime import datetime


class NewsArticleScraper:
    def __init__(self, url):
        self.url = url

    def scrape(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        for article in soup.find_all('article'):
            headline = article.find('h2').text.strip()
            summary = article.find('p').text.strip()
            articles.append({
                'headline': headline,
                'summary': summary
            })
        return articles


class TextPreprocessor:
    def __init__(self):
        self.stop_words = stopwords.words('english')
        self.stemmer = PorterStemmer()

    def preprocess(self, text):
        # Convert to lowercase
        text = text.lower()

        # Tokenize the text
        tokens = word_tokenize(text)

        # Remove stopwords and stem tokens
        filtered_tokens = [self.stemmer.stem(
            token) for token in tokens if token not in self.stop_words]

        return filtered_tokens


class ArticleAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def calculate_tfidf(self, corpus):
        tfidf_matrix = self.vectorizer.fit_transform(corpus)
        return tfidf_matrix

    def calculate_similarity(self, tfidf_matrix):
        similarity_matrix = cosine_similarity(tfidf_matrix)
        return similarity_matrix


class ArticleClusterer:
    def __init__(self, n_clusters):
        self.kmeans = KMeans(n_clusters=n_clusters)

    def cluster_articles(self, similarity_matrix):
        self.kmeans.fit(similarity_matrix)
        labels = self.kmeans.labels_
        return labels


class UserProfile:
    def __init__(self, user_id, interests):
        self.user_id = user_id
        self.interests = interests
        self.articles_read = []

    def read_article(self, article_id):
        self.articles_read.append(article_id)


class RecommendationEngine:
    def __init__(self, users, articles, similarity_matrix):
        self.users = users
        self.articles = articles
        self.similarity_matrix = similarity_matrix

    def get_recommendations(self, user_id):
        user = self.users[user_id]
        articles_read = user.articles_read
        article_scores = {}

        for article_id in range(len(self.articles)):
            if article_id not in articles_read:
                score = sum([self.similarity_matrix[article_id][read_id]
                            for read_id in articles_read])
                article_scores[article_id] = score

        sorted_articles = sorted(
            article_scores.items(), key=lambda x: x[1], reverse=True)
        recommended_article_ids = [
            article_id for article_id, _ in sorted_articles]

        return recommended_article_ids


class NotificationManager:
    def __init__(self):
        self.notifications = []

    def send_notification(self, user_id, message):
        timestamp = datetime.now()
        self.notifications.append({
            'timestamp': timestamp,
            'user_id': user_id,
            'message': message
        })

    def get_user_notifications(self, user_id):
        user_notifications = [
            notification for notification in self.notifications if notification['user_id'] == user_id]
        return user_notifications


class ArticleSaver:
    def __init__(self):
        self.saved_articles = []

    def save_article(self, user_id, article_id):
        self.saved_articles.append({
            'user_id': user_id,
            'article_id': article_id
        })

    def get_user_saved_articles(self, user_id):
        user_saved_articles = [
            saved_article for saved_article in self.saved_articles if saved_article['user_id'] == user_id]
        return user_saved_articles


def news_article_recommender():
    url = "https://example.com/news"

    scraper = NewsArticleScraper(url)
    articles = scraper.scrape()

    preprocessor = TextPreprocessor()
    preprocessed_corpus = [preprocessor.preprocess(
        article['summary']) for article in articles]

    analyzer = ArticleAnalyzer()
    tfidf_matrix = analyzer.calculate_tfidf(preprocessed_corpus)

    clusterer = ArticleClusterer(n_clusters=3)
    similarity_matrix = analyzer.calculate_similarity(tfidf_matrix)
    labels = clusterer.cluster_articles(similarity_matrix)

    # Create user profiles
    user1 = UserProfile(1, ['technology', 'science'])
    user2 = UserProfile(2, ['politics', 'economy'])
    user3 = UserProfile(3, ['sports', 'entertainment'])

    users = {
        1: user1,
        2: user2,
        3: user3
    }

    # Initialize recommendation engine
    recommendation_engine = RecommendationEngine(
        users, articles, similarity_matrix)

    # User reads articles and receive notifications
    user1.read_article(recommendation_engine.get_recommendations(1)[0])
    user2.read_article(recommendation_engine.get_recommendations(2)[1])
    user3.read_article(recommendation_engine.get_recommendations(3)[2])

    # Initialize notification manager
    notification_manager = NotificationManager()

    # Send notifications to users
    notification_manager.send_notification(1, "New articles available!")
    notification_manager.send_notification(2, "New articles available!")
    notification_manager.send_notification(3, "New articles available!")

    # Initialize article saver
    article_saver = ArticleSaver()

    # Save articles for users
    article_saver.save_article(1, user1.articles_read[0])
    article_saver.save_article(2, user2.articles_read[0])
    article_saver.save_article(3, user3.articles_read[0])

    # Get user notifications and saved articles
    user1_notifications = notification_manager.get_user_notifications(1)
    user2_saved_articles = article_saver.get_user_saved_articles(2)
    user3_notifications = notification_manager.get_user_notifications(3)

    # Print results
    print("User 1 recommendations:", recommendation_engine.get_recommendations(1))
    print("User 1 notifications:", user1_notifications)

    print("User 2 recommendations:", recommendation_engine.get_recommendations(2))
    print("User 2 saved articles:", user2_saved_articles)

    print("User 3 recommendations:", recommendation_engine.get_recommendations(3))
    print("User 3 notifications:", user3_notifications)


news_article_recommender()
