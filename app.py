# app.py
import pandas as pd
import streamlit as st

from news_trend_analysis import NewsTrendAnalysis


def get_user_inputs():
    """
    Capture user inputs for API key, topic of interest, start and end date.

    Returns:
        tuple: API key, topic, from date, to date, or None for each if input validation fails
    """
    from_date_default = pd.to_datetime("today") - pd.Timedelta(days=30)
    to_date_default = pd.to_datetime("today")

    api_key = st.text_input("Enter your Guardian API key")
    topic = st.text_input("Enter the topic of interest")
    from_date = st.date_input("Select the start date", value=from_date_default)
    to_date = st.date_input("Select the end date", value=to_date_default)

    return api_key, topic, from_date, to_date


def analyze_trends_df(api_key, topic, from_date, to_date):
    """
    Analyze trends based on user inputs and return the analyzed DataFrame and analyzer object.

    Returns:
        DataFrame, NewsTrendAnalysis: Analyzed dataframe and analyzer object
    """
    try:
        analyzer = NewsTrendAnalysis(api_key, topic, from_date, to_date)
        df = analyzer.analyze_trends()

        if df is None:
            st.write("No data returned from the API.")
        else:
            display_results(df, analyzer)

        return df, analyzer
    except Exception as e:
        st.error(f"Error in analyzing trends: {e}")
        return None, None


def display_results(df, analyzer):
    """
    Display sentiment scores, line chart of sentiment scores, table of articles, and API rate limits.

    Args:
        df (DataFrame): Analyzed dataframe
        analyzer (NewsTrendAnalysis): Analyzer object
    """
    # Display the average sentiment scores
    st.write("Average sentiment score:", df["sentiment"].mean())
    st.write(
        """Please note that the sentiment score is calculated using the VADER sentiment analysis tool, which is a lexicon and rule-based sentiment analysis tool that is specifically attuned to sentiments expressed in social media. It gives a compound score between -1 (most extreme negative) and +1 (most extreme positive) which can be used to gauge the sentiment of a text."""
    )

    # Display the line chart of sentiment scores
    st.subheader("Sentiment Score by Day")
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    weekly_df = df["sentiment"].resample("W").mean()
    st.line_chart(weekly_df)

    # Display the table of articles
    st.subheader("Articles Used in the Sentiment Analysis")
    st.write(df[["title", "author", "url", "sentiment"]])

    # Display the API rate limits
    st.subheader("API Rate Limits Based on Current Usage")
    rate_limits = analyzer.check_api_limits()
    st.write(rate_limits)


def write_df_to_csv(df, filename="news_trend_analysis.csv"):
    """
    Write DataFrame to a CSV file.

    Args:
        df (DataFrame): DataFrame to be written to CSV
        filename (str): Name of the file to be saved. Default is "news_trend_analysis.csv"
    """
    try:
        df.to_csv(filename, index=False)
    except Exception as e:
        st.error(f"Error writing DataFrame to CSV: {e}")


def save_to_csv(df):
    """
    Save DataFrame to a CSV file.

    Args:
        df (DataFrame): DataFrame to be saved
    """
    if st.button("Save to CSV"):
        filename = st.text_input("Enter a filename", value="news_trend_analysis.csv")
        write_df_to_csv(df, filename)
        st.success(f"Saved to {filename}")


def main():
    st.title("News Sentiment")

    api_key, topic, from_date, to_date = get_user_inputs()

    # proceed only if inputs are valid
    if all([api_key, topic, from_date, to_date]):
        if st.button("Analyze"):
            df, analyzer = analyze_trends_df(api_key, topic, from_date, to_date)

            # Save the DataFrame to a CSV file
            if df is not None:
                save_to_csv(df)


if __name__ == "__main__":
    main()
