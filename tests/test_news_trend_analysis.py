import pytest
import requests
from unittest.mock import patch, Mock
from news_trend_analysis import NewsTrendAnalysis


class TestNewsTrendAnalysis:
    @pytest.fixture
    def mock_response(self):
        return {
            "response": {
                "pages": 2,
                "results": [
                    {
                        "id": "1",
                        "webUrl": "https://test.com/1",
                        "fields": {
                            "body": "Test body 1",
                            "headline": "Test headline 1",
                            "byline": "Test byline 1",
                            "firstPublicationDate": "2023-05-28T00:00:00Z",
                        },
                    },
                    # Add more mock results as needed...
                ],
            }
        }

    @patch.object(requests.Session, "get")
    def test_fetch_data(self, mock_get, mock_response):
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = mock_response

        nta = NewsTrendAnalysis("test_key", "test_topic", "2023-05-28", "2023-05-29")
        result = nta.fetch_data()
        assert len(result) == 2
        assert result[0]["id"] == "1"

    @patch.object(requests.Session, "get")
    def test_analyze_trends(self, mock_get, mock_response):
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = mock_response

        nta = NewsTrendAnalysis("test_key", "test_topic", "2023-05-28", "2023-05-29")
        df = nta.analyze_trends()
        assert len(df) == 2
        assert df["id"][0] == "1"
        assert (
            df["sentiment"].isnull().sum() == 0
        )  # check that sentiment was calculated for all rows

    @patch.object(requests.Session, "get")
    def test_check_api_limits(self, mock_get):
        mock_headers = {
            "X-RateLimit-Limit-day": "1000",
            "X-RateLimit-Remaining-minute": "50",
            "X-RateLimit-Limit-minute": "100",
            "X-RateLimit-Remaining-day": "950",
            "X-Kong-Upstream-Latency": "123",
            "X-Kong-Proxy-Latency": "321",
        }

        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.headers = mock_headers

        nta = NewsTrendAnalysis("test_key", "test_topic", "2023-05-28", "2023-05-29")
        limits = nta.check_api_limits()
        assert limits["X-RateLimit-Limit-day"] == "1000"
