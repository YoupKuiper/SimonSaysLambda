from context import dbhandler

table = dbhandler.getDB("template")


dictLambda = {
    "AMIIDLookup": {
      "Id": "AWS::Lambda::Function",
      "Properties": {
        "Handler": "index.handler",
        "Role": { "Fn::GetAtt" : ["LambdaExecutionRole", "Arn"] },
        "Code": {
          "S3Bucket": "lambda-functions",
          "S3Key": "amilookup.zip"
        },
        "Runtime": "nodejs4.3",
        "Timeout": 25,
        "TracingConfig": {
          "Mode": "Active"
        }
      }
    }
}

dictEC2 = {"MyEC2Instance" : {
         "Id" : "AWS::EC2::Instance",
         "Properties" : {
            "ImageId" : "ami-79fd7eee",
            "KeyName" : "testkey",
            "BlockDeviceMappings" : [
               {
                  "DeviceName" : "/dev/sdm",
                  "Ebs" : {
                     "VolumeType" : "io1",
                     "Iops" : "200",
                     "DeleteOnTermination" : "false",
                     "VolumeSize" : "20"
                  }
               },
               {
                  "DeviceName" : "/dev/sdk",
                  "NoDevice" : {}
               }
            ]
         }
      }}

dictBucket = {
    "HelloBucket": {
      "Id": "AWS::S3::Bucket"
    }
}

dictDB = {
    "DynamoDB": {
        "Properties": {
                "AttributeDefinitions": [
                    {
                        'AttributeName': 'Type',
                        'AttributeType': 'S'
                    },
                ],
                "TableName": 'TestDBForCloudFormation',
                "KeySchema": [
                    {
                        'AttributeName': 'Type',
                        'KeyType': 'HASH'
                    },
                ],
                "ProvisionedThroughput": {
                    'ReadCapacityUnits': 123,
                    'WriteCapacityUnits': 123
                },
        },
        "Id": "AWS::DynamoDB::Table"
    }
}

table.put_item(Item={"Id": "s3", "json": dictBucket})
table.put_item(Item={"Id": "dynamodb", "json": dictDB})
table.put_item(Item={"Id": "ec2", "json": dictEC2})
table.put_item(Item={"Id": "lambda", "json": dictLambda})
