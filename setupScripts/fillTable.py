import boto3
import json

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

DB_NAME = 'SimonSaysCFNTemplates'
table = dynamodb.Table(DB_NAME)

dictTemp = {
    "VPC": {
        "Properties": {
            "CidrBlock": "10.0.0.0/16"
        },
        "Type": "AWS::EC2::VPC"
    }
}

dictTemp2 = {
    "DynamoDB": {
        "Properties": {
            "AttributeDefinitions": [
                {
                    "AttributeName": "type",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "JSON",
                    "AttributeType": "S"
                }
            ],
            "KeySchema": [
                {
                    "AttributeName": "type",
                    "KeyType": "RANGE"
                },
                {
                    "AttributeName": "JSON",
                    "KeyType": "RANGE"
                }
            ],
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            }
        },
        "Type": "AWS::DynamoDB::Table"
    }
}


dictTemp3 = {
  "mainLambda": {
    "Type": "AWS::Lambda::Function",
    "Properties": {
      "Code": {
        "S3Bucket": "projectsourcelambda",
        "S3Key": "myFunctionName.zip"
      },
      "Handler": "myFunctionName/lambda_function.lambda_handler",
      "Role": "arn:aws:iam::835483671006:role/lambda_basic_execution",
      "Runtime": "python3.6"
    }
  }
}

dicts = [dictTemp, dictTemp2, dictTemp3]

table.put_item(Item={"Type": "temp", "json": dictTemp})
table.put_item(Item={"Type": "temp2", "json": dictTemp2})
table.put_item(Item={"Type": "temp3", "json": dictTemp3})
