import boto3
import os
from git import Repo
from git import Git
import zipfile

print(os.getcwd())

BUCKET_NAME = "awscodepipelinetestbucketcf"

cloudFormationClient = boto3.client('cloudformation')
s3 = boto3.resource('s3')

projectName = "test"
stackName = 'teststack'
stackNamePL = 'teststack'
repoName = 'testrepo'

jsonFile = open(
    "/Users/spreng/development/SimonSaysLambda/templates/repoTemplate.json")
input = jsonFile.read()

response = cloudFormationClient.create_stack(
        StackName=stackName,
        TemplateBody=str(input),
        Parameters=[
            {
                "RepositoryName": repoName
                },
                ])

response = cloudFormationClient.describe_stacks(
    StackName=stackName,
)

while response['Stacks'][0]['StackStatus'] == "CREATE_IN_PROGRESS":
    response = cloudFormationClient.describe_stacks(StackName=stackName)

GIT_SSH_KEY = os.path.expanduser('~/.ssh/id_rsa')
git_ssh_cmd = 'ssh -i %s' % GIT_SSH_KEY

with Git().custom_environment(GIT_SSH_COMMAND=git_ssh_cmd):
    newrepo = Repo.clone_from(
        "ssh://git-codecommit.eu-west-1.amazonaws.com/v1/repos/pipelineTestRepo",
        "/Users/spreng/development/newrepo")

s3.Bucket(BUCKET_NAME).download_file("test.zip", "test.zip")

zip_ref = zipfile.ZipFile('test.zip', 'r')
zip_ref.extractall("/Users/spreng/development/newrepo/")
zip_ref.close()

newrepo.git.add("/Users/spreng/development/newrepo/*")
newrepo.git.commit('-m', 'test to see if python script works')
newrepo.git.push()

jsonFile = open(
    "/Users/spreng/development/SimonSaysLambda/templates/completeTemplate.json")
input = jsonFile.read()

response = cloudFormationClient.update_stack(
        StackName=stackName,
        TemplateBody=str(input),
        Parameters=[
            {
                "RepositoryName": repoName,
                "ProjectName": projectName,
                "StackName": stackNamePL
                },
                ])
