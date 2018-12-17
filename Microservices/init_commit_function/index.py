import json
import os
import cfnresponse
import boto3
import zipfile

ROOTDIR = "/tmp/"


def lambda_handler(event, context):

    # Setup clients for services
    lexClient = boto3.client('lex-models')
    s3Client = boto3.resource('s3')
    result = cfnresponse.FAILED

    # If the cfn request is a delete, delete the created bot
    if event["RequestType"] == "Delete":
        response = lexClient.delete_bot(
            name="SimonSays"
                )
        result = cfnresponse.SUCCESS
        return cfnresponse.send(event, context, result, {})
    # In the case of an update, there is nothing to do
    elif event["RequestType"] == "Update":
        result = cfnresponse.SUCCESS
        return cfnresponse.send(event, context, result, {})
    # In the case of a create setup the required variables
    else:
        bucketName = event["ResourceProperties"]["BucketName"]
        contentZipName = event["ResourceProperties"]["ContentZipName"]
        lambdaARN = event["ResourceProperties"]["LambdaARN"]

        # Download the file
        os.chdir(ROOTDIR)
        try:
            s3Client.Bucket(bucketName).download_file(contentZipName, contentZipName)
        except Exception as e:
            print(e)
            return cfnresponse.send(event, context, result, {})

        try:
            templatefile = open("/tmp/" + contentZipName, "r")
            template = templatefile.read()
            templateDict = json.loads(template)
            # Edit the proper Lambda ARN into the template
            for intent in templateDict["resource"]["intents"]:
                if "fulfillmentActivity" in intent:
                    fulfillmentActivity = intent["fulfillmentActivity"]
                    if "codeHook" in fulfillmentActivity:
                        codeHook = fulfillmentActivity["codeHook"]
                        codeHook["uri"] = lambdaARN
            print(templateDict)
        except Exception as e:
            print(e)
            return cfnresponse.send(event, context, result, {})

        try:
            zf = zipfile.ZipFile('zipfile_write.zip', mode='w')
            zf.write(contentZipName, json.dumps(templateDict))
            zf.close()
        except Exception as e:
            print(e)
            return cfnresponse.send(event, context, result, {})

        try:
            zipbot = open("/tmp/" + "zipfile_write.zip", "rb")
            zipbotdata = zipbot.read()
            response = lexClient.start_import(
                payload=zipbotdata,
                resourceType='BOT',
                mergeStrategy='OVERWRITE_LATEST'
                )

            while(response['importStatus'] == 'IN_PROGRESS'):
                response = lexClient.get_import(importId=response['importId'])

            result = cfnresponse.SUCCESS
        except Exception as e:
            print(e)
            return cfnresponse.send(event, context, result, {})

    cfnresponse.send(event, context, result, {})
