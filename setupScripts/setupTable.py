import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

table = dynamodb.create_table(
    AttributeDefinitions=[
        {
            'AttributeName': 'Type',
            'AttributeType': 'S'
        },
    ],
    TableName='SimonSaysCFNTemplates',
    KeySchema=[
        {
            'AttributeName': 'Type',
            'KeyType': 'HASH'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 123,
        'WriteCapacityUnits': 123
    }
)
