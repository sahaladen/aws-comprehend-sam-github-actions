import os
import json
import boto3

def handler(event, context):
    client = boto3.client('comprehend')
    body = event["body"]

    # Detect sentiment
    sentiment_response = client.detect_sentiment(LanguageCode="en", Text=body)

    # Detect toxic content
    toxic_response = client.detect_toxic_content(
        TextSegments=[{'Text': body}],
        LanguageCode='en'
    )

    # Extract relevant data
    toxic_results = toxic_response.get('ResultList', [])

    formatted_result = {
        "message": "Content analysis result",
        "input_text": body,
        "sentiment": {
            "overall": sentiment_response['Sentiment'],
            "scores": sentiment_response['SentimentScore']
        },
        "toxicity": {
            "labels": toxic_results[0].get('Labels', []) if toxic_results else [],
            "toxicity_score": toxic_results[0].get('Toxicity', None) if toxic_results else None
        }
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(formatted_result, indent=2)
    }