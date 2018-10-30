import boto3, os, shutil

cloudFormationClient = boto3.client('cloudformation')

stackName = 'teststack'

response = cloudFormationClient.delete_stack(
        StackName=stackName,
)
