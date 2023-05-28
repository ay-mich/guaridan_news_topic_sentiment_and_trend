# Guaridan Topic Sentiment and Trend

Analyze the sentiment trend of news articles on a specific topic over a selected time range using the Guardian's API. The sentiment analysis is performed using the NLTK library's VADER sentiment analysis tool.

## Prerequisites

The application requires the following software and libraries:

- Python 3.7 or higher
- pandas
- requests
- nltk
- beautifulsoup4
- streamlit

## Installation

Clone the repository to your local system:

`git clone <repository_url>`

Navigate into the cloned repository:

`cd <repository_folder>`

Install the required dependencies using pip:

`pip install -r requirements.txt`

## Usage

The application's user interface is provided by Streamlit. To use the application:

1. Run the application: `streamlit run app.py`

2. Open a web browser and navigate to the URL shown in your terminal (usually http://localhost:8501).

3. Follow the prompts in the Streamlit interface to enter your Guardian API key, the topic of interest, and select the date range for analysis.

4. Click the 'Analyze' button to fetch the data and display the results.

The results include:

- Average sentiment score of the articles fetched.
- A line chart of the sentiment score by day.
- A table displaying the articles used in the sentiment analysis.
- API rate limits based on current usage.
  The application provides an option to save the analyzed data as a CSV file. To do so, click the 'Save to CSV' button after analyzing the data.

## Modules

The application is composed of two primary modules:

**news_trend_analysis.py**

This module contains the NewsTrendAnalysis class, the application's backbone. It fetches data from the Guardian's API, processes the articles, and performs sentiment analysis on them using the NLTK library's VADER sentiment analysis tool. It also checks the API usage limits.

**app.py**

This module builds the application's user interface using Streamlit. It includes functions to:

- Capture user inputs (API key, topic, date range).
- Fetch and analyze data based on user inputs.
- Display the analysis results.
- Save the analysis data to a CSV file.

## The Guardian API

To use this application, you need an API key from The Guardian. Go [here](https://open-platform.theguardian.com/documentation) to register for an API key. This key is for non-commercial usage of the content, such as student dissertations, hackathons, and nonprofit app developers.

API key limits for developers:

- Up to 1 call per second
- Up to 500 calls per day
- Access to article text
- Access to over 1,900,000 pieces of content
- Free for non-commercial usage

## Contributing

Contributions are welcomed. If you find a bug or have a feature request, please open an issue. If you want to contribute code, please open a pull request.

## License

This project is licensed under the terms of the MIT license.
