import boto3
import os
import zipfile
import cfnresponse
import json
import yaml


FILEDIR = "/tmp/files/"
ROOTDIR = "/tmp/"
s3Client = boto3.resource('s3')
codecommitClient = boto3.client('codecommit')


def lambda_handler(event, context):
    if event['RequestType'] == 'Delete' or event['RequestType'] == 'Update':
        result = cfnresponse.SUCCESS
        return cfnresponse.send(event, context, result, {})

    result = cfnresponse.FAILED

    #Download zip to lambda
    try:
        bucketName = event["ResourceProperties"]["BucketName"]
        contentZipName = event["ResourceProperties"]["ContentZipName"]
        projectName = event["ResourceProperties"]["ProjectName"]
        os.chdir(ROOTDIR)
        s3Client.Bucket(bucketName).download_file(contentZipName, contentZipName)
    except Exception as e:
        print(e)
        return cfnresponse.send(event, context, result, {})

    #Unpack the zipfile
    try:
        zip_ref = zipfile.ZipFile(contentZipName, 'r')
        zip_ref.extractall(FILEDIR)
        zip_ref.close()
    except Exception as e:
        print(e)
        return cfnresponse.send(event, context, result, {})


    #Create initial commit
    try:
        repoName = event["ResourceProperties"]["RepositoryName"]
        readmeContent = 'This repository is provisioned by AWS lambda'
        initialCommit = codecommitClient.put_file(repositoryName=repoName, branchName='master', fileContent=readmeContent, filePath='readme.md')
        commitId = initialCommit['commitId']
    except Exception as e:
        print(e)
        return cfnresponse.send(event, context, result, {})


    #Write unpacked zip to codeCommit
    try:
        for filename in os.listdir(FILEDIR):
            in_file = open("/tmp/files/" + filename, "rb")
            data = in_file.read()
            if filename == "template.json":
                datajson = json.loads(data)
                datajson["Parameters"]["ProjectName"]["Default"] = projectName
                data = json.dumps(datajson, sort_keys=False, indent=4, separators=(',', ':'))
            elif filename == "buildspec.yml":
                yamltojson = yaml.load(data)
                yamltojson['phases']['post_build']['commands'][0] = yamltojson['phases']['post_build']['commands'][0].replace("PIPELINE_BUCKET", "codepipeline-" + projectName + "-artifactbucket")
                data = yaml.dump(yamltojson)
            in_file.close()
            response = codecommitClient.put_file(repositoryName=repoName, branchName='master', fileContent=data ,filePath=filename, parentCommitId=commitId)
            commitId = response['commitId']
    except Exception as e:
        print(e)
        return cfnresponse.send(event, context, result, {})


    result = cfnresponse.SUCCESS
    cfnresponse.send(event, context, result, {})
