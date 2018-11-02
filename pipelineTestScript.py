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
    "/Users/spreng/development/SimonSaysLambda/templates/new/test.json")
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

print("Creating repo...")
GIT_SSH_KEY = os.path.expanduser('~/.ssh/id_rsa')
git_ssh_cmd = 'ssh -i %s' % GIT_SSH_KEY

with Git().custom_environment(GIT_SSH_COMMAND=git_ssh_cmd):
    newrepo = Repo.clone_from(
        "ssh://git-codecommit.eu-west-1.amazonaws.com/v1/repos/TestProjectRepo",
        "/Users/spreng/development/newrepo")

print("Repo created...")

print("Getting necessary files...")

s3.Bucket(BUCKET_NAME).download_file("test.zip", "test.zip")

print("Files downloaded")

zip_ref = zipfile.ZipFile('test.zip', 'r')
zip_ref.extractall("/Users/spreng/development/newrepo/")
zip_ref.close()

newrepo.git.add("/Users/spreng/development/newrepo/*")
shutil.copyfile("/Users/spreng/development/SimonSaysLambda/index.js","/Users/spreng/development/newrepo/index.js")
newrepo.git.add("/Users/spreng/development/newrepo/index.js")
newrepo.git.commit('-m', 'Test using python script')
newrepo.git.push()

input("Press Enter to delete stack")

print("Deleting the created stack and repo")

response = cloudFormationClient.delete_stack(
        StackName=stackName)
response = cloudFormationClient.delete_stack(
        StackName="TestProjectStack"
)

shutil.rmtree('/Users/spreng/development/newrepo/')
