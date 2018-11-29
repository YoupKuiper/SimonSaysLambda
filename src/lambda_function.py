import boto3
from TemplateBuilder import TemplateBuilder
import os
import sys
import json
import time
from dbhandler import dbhandler

cloudFormationClient = boto3.client('cloudformation')
lexBotClient = boto3.client('lex-models')
t = TemplateBuilder()

projTable = dbhandler.getDB("project")


# Map intents to the right handler functions
def lambda_handler(event, context):
    print(event)
    currentIntent = event['currentIntent']['name']
    if currentIntent == "CreateProject":
        return createProject(event)
    elif currentIntent == "AddResources":
        return addResourcesToProject(event)
    elif currentIntent == "DeployProject":
        return deployProject(event)
    elif currentIntent == "GreetUser":
        return greetUser(event)
    elif currentIntent == "HelpFunction":
        return HelpUser(event)
    else:
        return buildLexResponse(1, "Error, unrecognized intent", None, None)


def buildLexResponse(error, message, sessionAttributesToAppend, event):
    if sessionAttributesToAppend is not None:
        sessionAttributes = appendSessionAttributes(
            event['sessionAttributes'], sessionAttributesToAppend)
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
        allowedresources.append(value['value'])
    return allowedresources


# Use the given name as the name for the project
def createProject(event):
    t.clear()
    projectName = event['currentIntent']['slots']['ProjectName']
    projectNameInput = event['inputTranscript']
    if (' ' in projectNameInput) is True:
        projectNameInput = projectNameInput.replace(" ", "-")
    message = f"Project {projectNameInput} has been created, please define the resources you want to have in your project"
    sessionAttributesToAppend = {"projectName": projectNameInput}
    projTable.put_item(Item={"ProjectName": projectName, "resources": []})

    return buildLexResponse(0, message, sessionAttributesToAppend, event)


# Create list of valid resources
def validateResources(resourcesToValidate):
    valid = []
    allowedResources = getAllowedResources()
    for resource in resourcesToValidate:
        if resource in allowedResources:
            valid.append(resource)
    return valid


# Create a well formed listed response for Lex to use
def listResponseBuilder(list):
    listresponse = ""
    for index, resource in enumerate(list):
        if index is (len(list) - 1) and (len(list)) != 1:
            listresponse = listresponse + " and " + resource
        elif index is 0:
            listresponse = listresponse + resource
        else:
            listresponse = listresponse + ", " + resource
    return listresponse


def addResourcesToProject(event):
    resources = list(event['currentIntent']['slots'].values())
    sessionAttributes = event['sessionAttributes']

    # If there is no project defined, return an error message
    if sessionAttributes['projectName'] is None:
        message = "Please define a project before adding resources"
        return buildLexResponse(0, message, None, event)

    projectName = sessionAttributes['projectName']

    # If resources already exist, add them all together
    if ("resources" in sessionAttributes):
        sessionResources = getResourcesFromSessionAttributesResources(sessionAttributes['resources'])
        resources.extend(sessionResources)

    # Validate resources
    valid = validateResources(resources)
    sessionAttributesToAppend = {}

    # Set the response message
    validString = listResponseBuilder(valid)
    if "pipeline" in valid and "lambda" not in valid:
        message = f"Adding a pipeline without a lambda is not supported."
    elif valid:
        # Append valid resources to session attributes
        sessionAttributesToAppend = {'resources': ",".join(valid)}

        # Add resources to template
        for resource in valid:
            t.addResource(resource)
        message = f"I have added {validString} to the project, you can deploy your project with: Deploy Project or add some other resources"
    else:
        message = "I didn't understand. Please restate your command."
    return buildLexResponse(0, message, sessionAttributesToAppend, event)


# Deploy a created project by launching the stack with cloudformation
def deployProject(event):
    projectName = event['sessionAttributes']['projectName']

    # Add project to projects table
    projTable.put_item(Item={"ProjectName": projectName,
                             "resources": t.getTemplate()})

    createStackFromTemplateBody(projectName, t.getTemplate(),  projectName, event)
    return buildLexResponse(0, f"Deployed {projectName}", {}, event)


def appendSessionAttributes(attributes, attributesToAppend):
    attributes.update(attributesToAppend)
    return attributes


def createStackFromURL(stackName, templateURL):
    response = cloudFormationClient.create_stack(
        StackName=stackName,
        TemplateURL=templateURL)

    print(response)


def createStackFromTemplateBody(stackName, templateBody, projectName, event):
    try:
        response = cloudFormationClient.create_stack(
            StackName=stackName,
            TemplateBody=str(templateBody),
            Capabilities = ['CAPABILITY_NAMED_IAM']
            )
    except Exception as e:
        print(str(e))
        return buildLexResponse(0, str(e), {}, event)

    print(response)

    response = cloudFormationClient.describe_stacks(StackName=stackName)

    while response['Stacks'][0]['StackStatus'] == "CREATE_IN_PROGRESS":
        time.sleep(10)
        response = cloudFormationClient.describe_stacks(StackName=stackName)

    return buildLexResponse(0, f"Project {projectName} has been created", {}, event)

# Function to gradually start a conversation


def greetUser(event):

    name = event['sessionAttributes']['name']

    message = "Hi, {}! I am the SimonSays bot. I can help you with the process " \
    "of creating AWS projects and deploying them. Create a project using the create" \
    "project command or say help for more information!".format(name)

    return buildLexResponse(0, message, {}, event)

# Function to help users during the process


def HelpUser(event):
    helpType = event['currentIntent']['slots']['Help']

    if helpType == 'projects':
        message = "You can create a project by saying 'create a project'."
    elif helpType == 'resources':
        message = "You can add resources after a project has been created by saying 'add', followed by the name of the resource you wish to add. You can also add multiple resources in a single command, try it out!"
    elif helpType == 'deployment':
        message = "Deploy a project after you are done adding resources to a created project by saying 'deploy project'"
    else:
        message = "I'm sorry, I cannot help you with {}. I can only help you with resources, projects and deployment. Please select one.".format(
            helpType)
        return elicit_slot(event['sessionAttributes'], event['currentIntent']['name'], event['currentIntent']['slots'], "Help", message)

    return buildLexResponse(0, message, {}, event)

def getResourcesFromSessionAttributesResources(sessionAttributesResourcesString):
    return sessionAttributesResourcesString.split(",")

def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': {
                'contentType': 'PlainText',
                'content': message
                },
            }
        }


if os.environ['DEBUG'] == "True":
    jsonFile = open(sys.argv[1], "r")
    input = jsonFile.read()
    inputDict = json.loads(input)
    lambda_handler(inputDict, None)
