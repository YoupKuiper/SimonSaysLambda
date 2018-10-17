import boto3
from TemplateBuilder import TemplateBuilder
import os
import sys
import json
from dbhandler import dbhandler

cloudFormationClient = boto3.client('cloudformation')
lexBotClient = boto3.client('lex-models')

projTable = dbhandler.getDB("project")


def lambda_handler(event, context):
    print(event)
    currentIntent = event['currentIntent']['name']
    if currentIntent == "CreateProject":
        return createProject(event)
    elif currentIntent == "AddResources":
        return buildTemplate(event)
    else:
        return buildLexResponse(1, "Error, unrecognized intent", None, None)


def buildLexResponse(error, message, sessionAttributesToAppend, event):
    if error:
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

def getAllowedResources():
    allowedresources = []
    response = lexBotClient.get_slot_type(
                                            name='Resources',
                                            version='3'
                                            )
    for value in response['enumerationValues']:
        allowedresources = allowedresources + (value['synonyms'])
    return allowedresources

def createProject(event):
    projectName = event['currentIntent']['slots']['ProjectName']
    message = f"Project {projectName} has been created, please define the resources you want to have in your project"
    sessionAttributesToAppend = {"projectName": projectName}
    projTable.put_item(Item={"ProjectName": projectName, "resources": []})

    return buildLexResponse(0, message, sessionAttributesToAppend, event)


def buildTemplate(event):
    t = TemplateBuilder()
    projectName = event['sessionAttributes']['projectName']
    strtest = ""
    resources = event['currentIntent']['slots']
    for resourceSlot in resources:
        resource = resources[resourceSlot]
        if resource in getAllowedResources():
            t.addResource(resource)
        else:
            buildLexResponse(1, f"Resource: {resource} not recognized",[],event)
        if list(resources).index(resourceSlot) is (len(resources) - 1):
            strtest = strtest + " and " + resource
        elif list(resources).index(resourceSlot) is 0:
            strtest = strtest + resource
        else:
            strtest = strtest + ", " + resource
    projTable.put_item(Item={"ProjectName": projectName, "resources": list(resources.values())})
    #createStackFromTemplateBody(projectName, t.getTemplate())
    message = f"The resources: {strtest} were added to project {projectName}."
    sessionAttributesToAppend = {}
    return buildLexResponse(0, message, sessionAttributesToAppend, event)


def appendSessionAttributes(attributes, attributesToAppend):
    attributes.update(attributesToAppend)
    return attributes


def createStackFromURL(stackName, templateURL):
    response = cloudFormationClient.create_stack(
        StackName=stackName,
        TemplateURL=templateURL)

    print(response)


def createStackFromTemplateBody(stackName, templateBody):
    response = cloudFormationClient.create_stack(
        StackName=stackName,
        TemplateBody=str(templateBody))

    print(response)


if os.environ['DEBUG'] == "True":
    jsonFile = open(sys.argv[1], "r")
    input = jsonFile.read()
    inputDict = json.loads(input)
    lambda_handler(inputDict, None)
