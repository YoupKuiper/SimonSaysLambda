import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):

    message = table.scan()

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Origin': '*',
            'Allow': 'GET, OPTIONS, POST',
            'Access-Control-Allow-Methods': 'GET, OPTIONS, POST',
            'Access-Control-Allow-Headers': '*'
        },
        'body': json.dumps(message['Items'], sort_keys=True, indent=4, separators=(',', ': '))
    }
