import os
import json
import boto3

def handler(event, context):

    client = boto3.client('comprehend')
    body = event["body"]
    '''sentiment = client.detect_sentiment(LanguageCode = "en", Text = body)'''
    response = client.detect_toxic_content(
        TextSegments=[
            {
                'Text': body
            },
        ],
        LanguageCode='en'
    )
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(
            {
                "message": "Toxic content analysis result:",
                "input_text": body,
                "detection_result": response
            },
            indent=4
        )
    }
