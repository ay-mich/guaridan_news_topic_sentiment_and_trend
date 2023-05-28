import nltk
import pandas as pd
import requests
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from requests import HTTPError

nltk.download("vader_lexicon")


class NewsTrendAnalysis:
    """
    A class to analyze news trends using The Guardian API and NLTK's VADER sentiment analysis.
    """

    def __init__(self, api_key, topic, from_date, to_date):
        self.api_key = api_key
        self.topic = topic
        self.from_date = from_date
        self.to_date = to_date
        self.base_url = "https://content.guardianapis.com/search"
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.session = requests.Session()

    def fetch_data(self):
        """
        Fetch data from The Guardian API.
        """
        params = {
            "q": self.topic,
            "from-date": self.from_date,
            "to-date": self.to_date,
            "api-key": self.api_key,
            "show-fields": "body,headline,byline,firstPublicationDate",
            "page": 1,
        }

        try:
            response = self.session.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            total_pages = data["response"]["pages"]
        except (requests.ConnectionError, requests.Timeout) as req_err:
            print(f"Request error occurred: {req_err}")
            return []
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return []
        except Exception as err:
            print(f"Other error occurred: {err}")
            return []

        results = [self.clean_result(r) for r in data["response"]["results"]]
        for page in range(2, total_pages + 1):
            params["page"] = page
            response = self.session.get(self.base_url, params=params)
            data = response.json()
            results.extend([self.clean_result(r) for r in data["response"]["results"]])

        return results

    @staticmethod
    def clean_result(result):
        """Clean a single API result by ensuring all fields exist."""
        result.setdefault("fields", {})
        for field in ["body", "headline", "byline", "firstPublicationDate"]:
            result["fields"].setdefault(field, "")
        return result

    def analyze_trends(self):
        """
        Analyze trends based on fetched data.
        """
        data = self.fetch_data()
        articles = []
        for d in data:
            fields = d.get("fields", {})
            article = {
                "id": d.get("id", ""),
                "title": fields.get("headline", ""),
                "date": pd.to_datetime(fields.get("firstPublicationDate", "")),
                "author": fields.get("byline", ""),
                "url": d.get("webUrl", ""),
                "body": fields.get("body", ""),
            }
            articles.append(article)
        df = pd.DataFrame(articles)
        df["sentiment"] = self.analyze_sentiment(df["body"])
        return df

    def analyze_sentiment(self, texts):
        """
        Analyze the sentiment of a given text.
        """
        cleaned_texts = texts.apply(
            lambda text: BeautifulSoup(text, "html.parser").get_text()
        )
        sentiment_scores = cleaned_texts.apply(self.sentiment_analyzer.polarity_scores)
        return sentiment_scores.apply(lambda score: score["compound"])

    def check_api_limits(self):
        """
        Check the API rate limits.
        """
        params = {
            "q": self.topic,
            "from-date": self.from_date,
            "to-date": self.to_date,
            "api-key": self.api_key,
            "show-fields": "body,headline,byline,firstPublicationDate",
        }
        response = self.session.get(self.base_url, params=params)
        rate_limits = {
            "X-RateLimit-Limit-day": response.headers.get("X-RateLimit-Limit-day"),
            "X-RateLimit-Remaining-minute": response.headers.get(
                "X-RateLimit-Remaining-minute"
            ),
            "X-RateLimit-Limit-minute": response.headers.get(
                "X-RateLimit-Limit-minute"
            ),
            "X-RateLimit-Remaining-day": response.headers.get(
                "X-RateLimit-Remaining-day"
            ),
            "X-Kong-Upstream-Latency": response.headers.get("X-Kong-Upstream-Latency"),
            "X-Kong-Proxy-Latency": response.headers.get("X-Kong-Proxy-Latency"),
        }
        return rate_limits
