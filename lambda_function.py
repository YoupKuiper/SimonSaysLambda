import boto3
from TemplateBuilder import TemplateBuilder
import os
import sys
import json

client = boto3.client('cloudformation')


def lambda_handler(event, context):
    print(context)
    currentIntent = event['currentIntent']['name']
    if currentIntent == "CreateProject":
        return createProject(event)
    elif currentIntent == "AddResources":
        return buildTemplate(event)
    else:
        return buildLexResponse(0, "Error, unrecognized intent", None, None)

def buildLexResponse(isRecognizedIntent, message, sessionAttributesToAppend, event):
    if not isRecognizedIntent:
        message = "Error, unrecognized intent"
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
    message = f"Project {projectName} has been created, please define the resources you want to have in your project"
    sessionAttributesToAppend = {"projectName": projectName}

    return buildLexResponse(1, message, sessionAttributesToAppend, event)


def buildTemplate(event):
    t = TemplateBuilder()
    projectName = event['sessionAttributes']['projectName']
    strtest = ""
    for resourceSlot in event['currentIntent']['slots']:
        resource = event['currentIntent']['slots'][resourceSlot]
        t.addResource(resource)
        strtest = strtest + " " + resource
    createStackFromTemplateBody(projectName, t.getTemplate())
    message = f"The resources:{strtest} were added to project {projectName}."
    sessionAttributesToAppend = {}
    return buildLexResponse(1, message, sessionAttributesToAppend, event)


def appendSessionAttributes(attributes, attributesToAppend):
    attributes.update(attributesToAppend)
    return attributes


def createStackFromURL(stackName, templateURL):
    response = client.create_stack(
        StackName=stackName,
        TemplateURL=templateURL)

    print(response)


def createStackFromTemplateBody(stackName, templateBody):
    response = client.create_stack(
        StackName=stackName,
        TemplateBody=str(templateBody))

    print(response)

if os.environ['DEBUG'] == "True":
    jsonFile = open(sys.argv[1], "r")
    input = jsonFile.read()
    inputDict = json.loads(input)
    lambda_handler(inputDict, None)
