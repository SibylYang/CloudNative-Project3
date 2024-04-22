import json
import boto3
import uuid

# Initialize the Boto3 DynamoDB client
dynamodb_client = boto3.client('dynamodb')

def handler(event, context):
    # Process order information specific to UK inventory
    print(event)
    # order_info = json.loads(event['Records'][0]['Sns']['Message'])
    sns_message = event['Records'][0]['Sns']['Message']
    if isinstance(sns_message, dict):
            order_info = sns_message
            print("order info is dict")
    else:
        try:
            order_info = json.loads(sns_message)
        except json.JSONDecodeError:
            # Handle the case where the message is not a valid JSON string
            print("SNS message is not a valid JSON string:", sns_message)
            # Return a response indicating failure
            return {
                'statusCode': 400,
                'body': json.dumps('Invalid message')
            }
    print(order_info)
    if order_info['location'] == 'UK':
        id_value = str(uuid.uuid4())
        # Add order to DynamoDB
        dynamodb_client.put_item(
            TableName='project3-UKDB-2ZF5NJ8Y2KUL', 
            Item={
                'id': {'S': id_value},
                'username': {'S': order_info.get('username')},
                'item': {'S': order_info.get('item')},
                'location': {'S': order_info.get('location')}
            }
        )
    print('UK inventory updated')
    return {
        'statusCode': 200,
        'body': json.dumps('UK inventory updated')
    }
