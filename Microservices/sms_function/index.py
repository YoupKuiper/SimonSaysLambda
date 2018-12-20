import cfnresponse
import boto3
import time


def handler(event, context):
    result = cfnresponse.FAILED

    if event['RequestType'] == 'Delete':
        result = cfnresponse.SUCCESS
        cfnresponse.send(event, context, result, {})
    else:
        try:
            userpoolid = event['ResourceProperties']['CognitoPool']
            AccessKey = event['ResourceProperties']['AccessKey']
            SecretKey = event['ResourceProperties']['SecretKey']
            phoneNumber = event['ResourceProperties']['PhoneNumber']
            print(event)
        except Exception as E:
            print(E)
            return cfnresponse.send(event, context, result, {})

        try:
            sendSMS(AccessKey, SecretKey, phoneNumber, userpoolid, "Test")
        except Exception as E:
            print(E)
            return cfnresponse.send(event, context, result, {})

        result = cfnresponse.SUCCESS
        return cfnresponse.send(event, context, result, {})



def sendSMS(AccessKey, SecretKey, number, message, sender):
    client = boto3.client(
        'sns',
        aws_access_key_id=AccessKey,
        aws_secret_access_key=SecretKey,
    )

    time.sleep(5)

    response = client.publish(
        PhoneNumber=number,
        Message=message,
        MessageAttributes={
            'AWS.SNS.SMS.SenderID': {
                'DataType': 'String',
                'StringValue': sender,
            }
        },
    )

    print('Request ID : ' + str(response['ResponseMetadata']['RequestId']))
    print('Status Code : ' + str(response['ResponseMetadata']['HTTPStatusCode']))
