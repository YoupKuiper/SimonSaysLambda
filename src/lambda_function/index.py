import json
import boto3
import os
import zipfile
import cfnresponse

FILEDIR = "/tmp/files/"
ROOTDIR = "/tmp/"
s3Client = boto3.resource('s3')
codecommitClient = boto3.client('codecommit')


def lambda_handler(event, context):

    #Download zip to lambda
    bucketName = event["ResourceProperties"]["BucketName"]
    contentZipName = event["ResourceProperties"]["ContentZipName"]
    os.chdir(ROOTDIR)
    s3Client.Bucket(bucketName).download_file(contentZipName, contentZipName)

    #Unpack the zipfile
    zip_ref = zipfile.ZipFile(contentZipName, 'r')
    zip_ref.extractall(FILEDIR)
    zip_ref.close()

    #Create initial commit
    repoName = event["ResourceProperties"]["RepositoryName"]
    readmeContent = 'This repository is provisioned by AWS lambda'
    initialCommit = codecommitClient.put_file(repositoryName=repoName, branchName='master', fileContent=readmeContent, filePath='readme.md')
    commitId = initialCommit['commitId']

    #Write unpacked zip to codeCommit
    for filename in os.listdir(FILEDIR):
        in_file = open("/tmp/files/" + filename, "rb")
        data = in_file.read()
        in_file.close()
        response = codecommitClient.put_file(repositoryName=repoName, branchName='master', fileContent=data ,filePath=filename, parentCommitId=commitId)
        commitId = response['commitId']

    result = cfnresponse.SUCCESS
    cfnresponse.send(event, context, result, {})