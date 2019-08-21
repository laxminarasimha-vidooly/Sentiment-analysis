# Sentiment-analysis

Objective: To provide sentiment analysis of the YouTube video comments

Business problem: Brands often require the sentiment on YouTube about their products and also the sentiment among other creators(UGC).
For this we need to give the sentiment analysis in Positive, Negative and Neutral attributes.

Tools: Python

Process:

1. First 500 comments of each video from YouTube will be gathered through API

2. Text processing is done to remove punctuations, non english characters, white space and special characters

3. Sentiment is analyzed by polarity method using TextBlob package

3. Video wise sentiment is consolidated and email is sent to the recipient

