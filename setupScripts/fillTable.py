import boto3
import json

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

DB_NAME = 'SimonSaysCFNTemplates'
table = dynamodb.Table(DB_NAME)

dictBucket = {
    "HelloBucket": {
      "Type": "AWS::S3::Bucket"
    }
}

dictDB = {
    "DynamoDB": {
        "Properties": {
                "AttributeDefinitions":[
                    {
                        'AttributeName': 'Type',
                        'AttributeType': 'S'
                    },
                ],
                "TableName":'TestDBForCloudFormation',
                "KeySchema":[
                    {
                        'AttributeName': 'Type',
                        'KeyType': 'HASH'
                    },
                ],
                "ProvisionedThroughput":{
                    'ReadCapacityUnits': 123,
                    'WriteCapacityUnits': 123
                },
        },
        "Type": "AWS::DynamoDB::Table"
    }
}



dicts = [dictBucket, dictDB]

table.put_item(Item={"Type": "s3", "json": dictBucket})
table.put_item(Item={"Type": "dynamodb", "json": dictDB})
