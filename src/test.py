from dbhandler import dbhandler
import boto3
import json

stackName="teststringtemplate"
cloudFormationClient = boto3.client('cloudformation')

table = dbhandler.getDB("template")

type = "LambdaDemo"

resource = table.get_item(Key={'Id': type})

item = resource["Item"]["json"]

print(item)
testitem = json.loads(item)
testitem.update({'Parameters' : {  "ProjectName": {
  "Default": "SvenTestBuild",
  "Type": "String"
}}})

print(testitem)

response = cloudFormationClient.create_stack(
        StackName=stackName,
        TemplateBody=str(testitem),
        Capabilities=[
        'CAPABILITY_IAM'],
        Parameters=[{
        "ParameterKey" : "ProjectName",
        "ParameterValue" : "Test"}])
