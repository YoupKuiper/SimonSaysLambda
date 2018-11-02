import boto3
from TemplateBuilder import TemplateBuilder
import os
import sys
import json
from dbhandler import dbhandler

cloudFormationClient = boto3.client('cloudformation')
lexBotClient = boto3.client('lex-models')
t = TemplateBuilder()

projTable = dbhandler.getDB("project")


def lambda_handler(event, context):
    print(event)
    currentIntent = event['currentIntent']['name']
    if currentIntent == "CreateProject":
        return createProject(event)
    elif currentIntent == "AddResources":
        return addResourcesToProject(event)
    elif currentIntent == "DeployProject":
        return deployProject(event)
    else:
        return buildLexResponse(1, "Error, unrecognized intent", None, None)


def buildLexResponse(error, message, sessionAttributesToAppend, event):
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


# Create a list of allowed resources
def getAllowedResources():
    allowedresources = []
    response = lexBotClient.get_slot_type(
                                            name='Resources',
                                            version='$LATEST'
                                            )
    for value in response['enumerationValues']:
        #allowedresources = allowedresources + (value['synonyms'])
        allowedresources.append(value['value'])
    return allowedresources


# Use the given name as the name for the project
def createProject(event):
    t.clear()
    projectName = event['currentIntent']['slots']['ProjectName']
    message = f"Project {projectName} has been created, please define the resources you want to have in your project"
    sessionAttributesToAppend = {"projectName": projectName}
    projTable.put_item(Item={"ProjectName": projectName, "resources": []})

    return buildLexResponse(0, message, sessionAttributesToAppend, event)


# Create list of valid resources
def validateResources(resourcesToValidate):
    valid = []
    allowedResources = getAllowedResources()
    for resourceSlot in resourcesToValidate:
        resource = resourcesToValidate[resourceSlot]
        if resource in allowedResources:
            valid.append(resource)
    return valid


def listResponseBuilder(list):
    listresponse = ""
    for resource in list:
        if list.index(resource) is (len(list) - 1) and (len(list)) != 1:
            listresponse = listresponse + " and " + resource
        elif list.index(resource) is 0:
            listresponse = listresponse + resource
        else:
            listresponse = listresponse + ", " + resource
    return listresponse


def addResourcesToProject(event):
    resources = event['currentIntent']['slots']
    sessionAttributes = event['sessionAttributes']
    projectName = sessionAttributes['projectName']

    # If resources already exist, add them all together
    if(hasattr(sessionAttributes, 'resources')):
        resources.extend(sessionAttributes['resources'])

    # Validate resources
    valid = validateResources(resources)

    print("valid")
    print(valid)

    # Append valid resources to session attributes
    sessionAttributesToAppend = {'resources': valid}

    # Add resources to template
    for resource in valid:
        t.addResource(resource)

    # Add project to projects table
    projTable.put_item(Item={"ProjectName": projectName, "resources": list(resources.values())})

    # Set the response message
    validString = listResponseBuilder(valid)
    if "pipeline" in resources and "lambda" not in resources:
        message = f"Adding a pipeline without a lambda is not supported."
    elif valid:
        message = f"I have added {validString} to the project, you can deploy your project with: Deploy Project or add some other resources"
    else:
        message = f"I didn't understand. Please restate your command."
    return buildLexResponse(0, message, sessionAttributesToAppend, event)


def deployProject(event):
    projectName = event['sessionAttributes']['projectName']
    createStackFromTemplateBody(projectName, t.getTemplate())
    return buildLexResponse(0, f"Deployed {projectName}", {}, event)


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
