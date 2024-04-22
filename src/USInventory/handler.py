import json
import boto3
import uuid
# Initialize the Boto3 DynamoDB client
dynamodb_client = boto3.client('dynamodb')

def handler(event, context):
    # Process order information specific to US inventory
    order_info = json.loads(event['Records'][0]['Sns']['Message'])
    if order_info.get('location') == 'US':
        # Add order to DynamoDB
        id_value = str(uuid.uuid4())
        dynamodb_client.put_item(
            TableName='project3-USDB-13DADSRGHQCVQ', 
            Item={
                'id': {'S': id_value},
                'username': {'S': order_info['username']},
                'item': {'S': order_info['item']},
                'location': {'S': order_info['location']}
            }
        )
    print('US inventory updated')
    return {
        'statusCode': 200,
        'body': json.dumps('US inventory updated')
    }
