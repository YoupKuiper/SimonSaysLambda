import boto3
import os
import sys
from git import Repo
from git import Git
import zipfile
import shutil
import time

print(os.getcwd())

BUCKET_NAME = "awscodepipelinetestbucketcf"

cloudFormationClient = boto3.client('cloudformation')
s3 = boto3.resource('s3')

projectName = "TestProject"

stackName = sys.argv[1]

jsonFile = open(
    "/Users/spreng/development/SimonSaysLambda/templates/newWebsite/APIGateway.json")
userInput = jsonFile.read()

print("Creating stack...")
response = cloudFormationClient.create_stack(
        StackName=stackName,
        TemplateBody=str(userInput),
        Capabilities=['CAPABILITY_NAMED_IAM'])

response = cloudFormationClient.describe_stacks(
    StackName=stackName,
)

print("CREATE_IN_PROGRESS")

while response['Stacks'][0]['StackStatus'] == "CREATE_IN_PROGRESS":
    time.sleep(5)
    response = cloudFormationClient.describe_stacks(StackName=stackName)

print("Stack created...")


input("Press Enter to delete stack")

print("Deleting the created stack")

response = cloudFormationClient.delete_stack(
        StackName=stackName)
