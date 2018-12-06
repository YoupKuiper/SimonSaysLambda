import os
import json
import cfnresponse

import boto3
from botocore.exceptions import ClientError
client = boto3.client('s3')
lambdaClient = boto3.client('lambda')

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
  logger.info("Received event: %s" % json.dumps(event))
  source_bucket = event['ResourceProperties']['SourceBucket']
  source_prefix = event['ResourceProperties'].get('SourcePrefix') or ''
  bucket = event['ResourceProperties']['Bucket']
  prefix = event['ResourceProperties'].get('Prefix') or ''
  APIUrl = event['ResourceProperties'].get('APIUrl') or ''

  result = cfnresponse.SUCCESS

  try:
    if event['RequestType'] == 'Create' or event['RequestType'] == 'Update':
      result = copy_objects(source_bucket, source_prefix, bucket, prefix, APIUrl)
    elif event['RequestType'] == 'Delete':
      print('deleting')
      result = lambdaClient.invoke(FunctionName='S3BucketDeletionService', InvocationType='RequestResponse', Payload=json.dumps(event['ResourceProperties']))
  except ClientError as e:
    logger.error('Error: %s', e)
    result = cfnresponse.FAILED

  cfnresponse.send(event, context, result, {})


def copy_objects(source_bucket, source_prefix, bucket, prefix, APIUrl):
  # Add api url to file in new bucket

  client.put_object(Body=APIUrl, Bucket=bucket, Key='js/config.js')

  # Copy files from the source to new bucket
  paginator = client.get_paginator('list_objects_v2')
  page_iterator = paginator.paginate(Bucket=source_bucket, Prefix=source_prefix)
  for key in {x['Key'] for page in page_iterator for x in page['Contents']}:
    dest_key = os.path.join(prefix, os.path.relpath(key, source_prefix))
    if not key.endswith('/'):
      print('copy {} to {}'.format(key, dest_key))
      client.copy_object(CopySource={'Bucket': source_bucket, 'Key': key}, Bucket=bucket, Key = dest_key)
  return cfnresponse.SUCCESS
