import os
import json
import boto3

def handler(event, context):
    client = boto3.client('comprehend')
    body = event["body"]

    # Detect sentiment
    sentiment = client.detect_sentiment(LanguageCode="en", Text=body)

    # Extract only the relevant parts (NOT the entire response)
    formatted_result = {
        "message": "Sentiment analysis result",
        "input_text": body,
        "sentiment": sentiment['Sentiment'],  # Just the sentiment value
        "scores": {
            "positive": sentiment['SentimentScore']['Positive'],
            "negative": sentiment['SentimentScore']['Negative'],
            "neutral": sentiment['SentimentScore']['Neutral'],
            "mixed": sentiment['SentimentScore']['Mixed']
        }
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(formatted_result, indent=2)  # Only call json.dumps ONCE
    }