import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

table = dynamodb.create_table(
    AttributeDefinitions=[
        {
            'AttributeName': 'Id',
            'AttributeType': 'S'
        },
    ],
    TableName='SimonSaysCFNTemplates',
    KeySchema=[
        {
            'AttributeName': 'Id',
            'KeyType': 'HASH'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 123,
        'WriteCapacityUnits': 123
    }
)

table2 = dynamodb.create_table(
    AttributeDefinitions=[
        {
            'AttributeName': 'ProjectName',
            'AttributeType': 'S'
        },
    ],
    TableName='SimonSaysProjects',
    KeySchema=[
        {
            'AttributeName': 'ProjectName',
            'KeyType': 'HASH'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 123,
        'WriteCapacityUnits': 123
    }
)
