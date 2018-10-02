import json
from troposphere import Ref, Template
import troposphere.ec2 as ec2

def lambda_handler(event, context):
    print(event)
    currentIntent = event['currentIntent']['name']
    if currentIntent == "CreateProject":
        return createProject(event)
    elif currentIntent == "AddDatabase":
        return addDatabase(event)
    elif currentIntent == "AddDefaultVPC":
        return addDefaultVPC(event)
    elif currentIntent == "AddCustomVPC":
        return addCustomVPC(event)
    else:
        return buildLexResponse(0, "Error, unrecognized intent", None, None)


def buildLexResponse(isRecognizedIntent, message, sessionAttributesToAppend, event):
    if not isRecognizedIntent:
        message: "Error, unrecognized intent"

    if sessionAttributesToAppend is not None:
        sessionAttributes = appendSessionAttributes(event['sessionAttributes'], sessionAttributesToAppend)
    else:
        sessionAttributes = event['sessionAttributes']

    return {
        "sessionAttributes": sessionAttributes,
        "dialogAction": {
            "type": "ElicitIntent",
            "message": {
                "contentType": "PlainText",
                "content": message
            },
        }
    }


def createProject(event):
    projectName = event['currentIntent']['slots']['ProjectName']
    message = f"Project {projectName} has been created, would you like a custom or a default VPC?"
    sessionAttributesToAppend = {"projectName": projectName}

    return buildLexResponse(1, message, sessionAttributesToAppend, event)


def addCustomVPC(event):
    amountOfPublicSubnets = event['currentIntent']['slots']['AmountOfPublicSubnets']
    amountOfPrivateSubnets = event['currentIntent']['slots']['AmountOfPrivateSubnets']

    sessionAttributesToAppend = {
        "VPC": "custom",
        "amountOfPublicSubnets": amountOfPublicSubnets,
        "amountOfPrivateSubnets": amountOfPrivateSubnets
    }
    projectName = event['sessionAttributes']['projectName']

    message = f"A custom VPC with {amountOfPublicSubnets} public subnets and {amountOfPrivateSubnets} private subnets has been added to project {projectName}"

    return buildLexResponse(1, message, sessionAttributesToAppend, event)


def addDefaultVPC(event):
    projectName = event['sessionAttributes']['projectName']
    message = f"The default VPC has been added to project {projectName}."
    sessionAttributesToAppend = {"VPC": "default"}
    buildCloudFormationTemplate()
    return buildLexResponse(1, message, sessionAttributesToAppend, event)


def addDatabase(event):
    print("asd")


def appendSessionAttributes(attributes, attributesToAppend):
    attributes.update(attributesToAppend)
    return attributes


def buildCloudFormationTemplate():
    t = Template()
    instance = ec2.Instance("myinstance")
    instance.ImageId = "ami-951945d0"
    instance.InstanceType = "t1.micro"
    t.add_resource(instance)
    print(t.to_json())

