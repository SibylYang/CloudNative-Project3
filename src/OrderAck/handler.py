import json
import os
import boto3

# Initialize the SNS client
sns_client = boto3.client('sns')

# -- Test on Github Action ---

def handler(event, context):
    # Parse the POST request body
    print(event)
    
    request_body = event['body']
    if request_body:
        try:
            request_data = json.loads(request_body)
        except json.JSONDecodeError as e:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid JSON format'})
            }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Request body is missing'})
        }
    print(request_data)

    # Retrieve SNS topic ARN from environment variable
    topic_arn = os.environ['ORDERTOPIC_TOPIC_ARN']

    # Publish message to SNS topic
    sns_client.publish(
        TopicArn=topic_arn,
        Message=json.dumps(request_data)
    )

    # Return response
    return {
        'statusCode': 200,
        'body': json.dumps('Order received and published to SNS')
    }
