from context import dbhandler

table = dbhandler.getDB("template")

dictLambda = {
  "mainLambda": {
    "Type": "AWS::Lambda::Function",
    "Properties": {
      "Code": {
        "S3Bucket": "projectsourcelambda",
        "S3Key": "myFunctionName.zip"
      },
      "Handler": "myFunctionName/lambda_function.lambda_handler",
      "Role": "arn:aws:iam::835483671006:role/lambda_basic_execution",
      "Runtime": "python3.6"
    }
  }
}

dictEC2 = {"MyEC2Instance" : {
         "Type" : "AWS::EC2::Instance",
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
      "Type": "AWS::S3::Bucket"
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
        "Type": "AWS::DynamoDB::Table"
    }
}

table.put_item(Item={"Type": "s3", "json": dictBucket})
table.put_item(Item={"Type": "dynamodb", "json": dictDB})
table.put_item(Item={"Type": "ec2", "json": dictEC2})
table.put_item(Item={"Type": "lambda", "json": dictLambda})
