import json
import cfnresponse
import boto3


def lambda_handler(event, context):
    print(event)
    result = cfnresponse.SUCCESS

    # if request type is delete or update, do nothing
    if event['RequestType'] == 'Delete' or event['RequestType'] == 'Update':
        return cfnresponse.send(event, context, result, {})

    # Get the name of the table
    tableName = event['ResourceProperties']['TableName']

    # Get the demo template
    demoContents = open('demo.json').read()
    demoJson = json.loads(demoContents)

    try:
        if 'Mappings' not in demoContents:
            demoJson.update({"Mappings": {}})
        if 'Parameters' not in demoContents:
            demoJson.update({"Parameters": {}})
        if 'Outputs' not in demoContents:
            demoJson.update({"Outputs": {}})

        resources = json.dumps(demoJson["Resources"])
        Mappings = json.dumps(demoJson["Mappings"])
        Parameters = json.dumps(demoJson["Parameters"])
        Outputs = json.dumps(demoJson["Outputs"])
        demo = "demo"

    except:
        print("Something went wrong while trying get the required information from the demo template")
        result = cfnresponse.FAILED
        return cfnresponse.send(event, context, result, {})

        # Put the demo template in the db
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(tableName)

        response = table.put_item(
            Item={"Id": demo, "json": demoContents, "json-resources": resources, "json-mappings": Mappings,
                  "json-parameters": Parameters, "json-outputs": Outputs}
        )
    except Exception as e:
        print("Something went wrong while trying to add the template to the database")
        print(e)
        print(demoJson)
        result = cfnresponse.FAILED
        return cfnresponse.send(event, context, result, {})

    return cfnresponse.send(event, context, result, {})
