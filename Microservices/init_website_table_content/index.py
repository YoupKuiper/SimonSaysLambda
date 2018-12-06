import json
import boto3
import cfnresponse

def lambda_handler(event, context):

    client = boto3.client('dynamodb')

    response = client.put_item(
    TableName=event["ResourceProperties"]["TableName"],
    Item={
        'Key': {"S": event["ResourceProperties"]["ProjectName"]}
    })

    result = cfnresponse.SUCCESS
    cfnresponse.send(event, context, result, {})
