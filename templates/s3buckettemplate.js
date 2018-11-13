{
  "AWSTemplateFormatVersion": "2010-09-09",
  "Description": "Creates a static website using S3 for the serverless web application demo",
  "Parameters": {
    "BucketName": {
      "Type": "String",
      "Description": "The name for the bucket hosting your website, e.g. 'wildrydes-yourname'"
    },
    "CodeBucket": {
      "Type": "String",
      "Default": "wildrydes-eu-west-1",
      "Description": "S3 bucket containing the code deployed by this template"
    },
    "CodeKeyPrefix": {
      "Type": "String",
      "Default": "WebApplication/1_StaticWebHosting",
      "Description": "Key prefix for resources referenced from the CodeBucket"
    }
  },
  "Metadata": {
    "AWS::CloudFormation::Interface": {
      "ParameterGroups": [
        {
          "Label": {
            "default": "Website Configuration"
          },
          "Parameters": [
            "BucketName"
          ]
        },
        {
          "Label": {
            "default": "Advanced Configuration"
          },
          "Parameters": [
            "CodeBucket",
            "CodeKeyPrefix"
          ]
        }
      ],
      "ParameterLabels": {
        "BucketName": {
          "default": "Website Bucket Name"
        }
      }
    }
  },
  "Resources": {
    "WebsiteBucket": {
      "Properties": {
        "BucketName": "BucketName",
        "WebsiteConfiguration": {
          "IndexDocument": "index.html"
        }
      },
      "Type": "AWS::S3::Bucket"
    },
    "WebsiteBucketPolicy": {
      "Properties": {
        "Bucket": "WebsiteBucket",
        "PolicyDocument": {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Effect": "Allow",
              "Principal": "*",
              "Action": "s3:GetObject",
              "Resource": "arn:aws:s3:::${WebsiteBucket}/*"
            }
          ]
        }
      },
      "Type": "AWS::S3::BucketPolicy"
    },
    "WebsiteContent": {
      "Properties": {
        "ServiceToken": "CopyS3ObjectsFunction.Arn",
        "SourceBucket": "CodeBucket",
        "SourcePrefix": "${CodeKeyPrefix}/website/",
        "Bucket": "WebsiteBucket"
      },
      "Type": "Custom::S3Objects"
    },
    "S3CopyRole": {
      "Type": "AWS::IAM::Role",
      "Properties": {
        "Path": "/wildrydes/",
        "AssumeRolePolicyDocument": {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Effect": "Allow",
              "Principal": {
                "Service": "lambda.amazonaws.com"
              },
              "Action": "sts:AssumeRole"
            }
          ]
        },
        "Policies": [
          {
            "PolicyName": "S3Access",
            "PolicyDocument": {
              "Version": "2012-10-17",
              "Statement": [
                {
                  "Sid": "AllowLogging",
                  "Effect": "Allow",
                  "Action": [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                  ],
                  "Resource": "*"
                },
                {
                  "Sid": "SourceBucketReadAccess",
                  "Effect": "Allow",
                  "Action": [
                    "s3:ListBucket",
                    "s3:GetObject"
                  ],
                  "Resource": [
                    "arn:aws:s3:::${CodeBucket}",
                    "arn:aws:s3:::${CodeBucket}/${CodeKeyPrefix}/*"
                  ]
                },
                {
                  "Sid": "DestBucketWriteAccess",
                  "Effect": "Allow",
                  "Action": [
                    "s3:ListBucket",
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:PutObjectAcl",
                    "s3:PutObjectVersionAcl",
                    "s3:DeleteObject",
                    "s3:DeleteObjectVersion",
                    "s3:CopyObject"
                  ],
                  "Resource": [
                    "arn:aws:s3:::${WebsiteBucket}",
                    "arn:aws:s3:::${WebsiteBucket}/*"
                  ]
                }
              ]
            }
          }
        ]
      }
    },
    "CopyS3ObjectsFunction": {
      "Properties": {
        "Description": "Copies objects from a source S3 bucket to a destination",
        "Handler": "index.handler",
        "Runtime": "python2.7",
        "Role": "S3CopyRole.Arn",
        "Timeout": 120,
        "Code": {
          "ZipFile": "import os\nimport json\nimport cfnresponse\n\nimport boto3\nfrom botocore.exceptions import ClientError\nclient = boto3.client('s3')\n\nimport logging\nlogger = logging.getLogger()\nlogger.setLevel(logging.INFO)\n\ndef handler(event, context):\n  logger.info(\"Received event: %s\" % json.dumps(event))\n  source_bucket = event['ResourceProperties']['SourceBucket']\n  source_prefix = event['ResourceProperties'].get('SourcePrefix') or ''\n  bucket = event['ResourceProperties']['Bucket']\n  prefix = event['ResourceProperties'].get('Prefix') or ''\n\n  result = cfnresponse.SUCCESS\n\n  try:\n    if event['RequestType'] == 'Create' or event['RequestType'] == 'Update':\n      result = copy_objects(source_bucket, source_prefix, bucket, prefix)\n    elif event['RequestType'] == 'Delete':\n      result = delete_objects(bucket, prefix)\n  except ClientError as e:\n    logger.error('Error: %s', e)\n    result = cfnresponse.FAILED\n\n  cfnresponse.send(event, context, result, {})\n\n\ndef copy_objects(source_bucket, source_prefix, bucket, prefix):\n  paginator = client.get_paginator('list_objects_v2')\n  page_iterator = paginator.paginate(Bucket=source_bucket, Prefix=source_prefix)\n  for key in {x['Key'] for page in page_iterator for x in page['Contents']}:\n    dest_key = os.path.join(prefix, os.path.relpath(key, source_prefix))\n    if not key.endswith('/'):\n      print 'copy {} to {}'.format(key, dest_key)\n      client.copy_object(CopySource={'Bucket': source_bucket, 'Key': key}, Bucket=bucket, Key = dest_key)\n  return cfnresponse.SUCCESS\n\ndef delete_objects(bucket, prefix):\n  paginator = client.get_paginator('list_objects_v2')\n  page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix)\n  objects = [{'Key': x['Key']} for page in page_iterator for x in page['Contents']]\n  client.delete_objects(Bucket=bucket, Delete={'Objects': objects})\n  return cfnresponse.SUCCESS\n"
        }
      },
      "Type": "AWS::Lambda::Function"
    }
  },
  "Outputs": {
    "WebsiteURL": {
      "Value": "WebsiteBucket.WebsiteURL"
    }
  }
}
