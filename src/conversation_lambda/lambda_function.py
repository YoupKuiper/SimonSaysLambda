import boto3
import os
import sys
import json
from dbhandler import dbhandler

lexBotClient = boto3.client('lex-models')
lambdaClient = boto3.client('lambda')
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
    projectName = event['currentIntent']['slots']['ProjectName']
    projectNameInput = event['inputTranscript']
    if (' ' in projectNameInput) is True:
        projectNameInput = projectNameInput.replace(" ", "-")

    sessionAttributesToAppend = {}

    if projectAlreadyExists(projectNameInput):
        message = f"Project {projectNameInput} already exists, so it cannot be created. What would you like to name your project instead?"
    else:
        message = f"Project {projectNameInput} has been created, please define the resources you want to have in your project"
        sessionAttributesToAppend = {"projectName": projectNameInput}

    return buildLexResponse(0, message, sessionAttributesToAppend, event)


def projectAlreadyExists(projectName):
    project = projTable.get_item(Key={'ProjectName': projectName})

    # If project already exists, it will be able to print
    # if 'Item' in project:
    #     return True
    # else:
    #     return False
    return False

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
    if 'projectName' not in sessionAttributes:
        message = "Please create a project before adding resources"
        return buildLexResponse(0, message, None, event)

    projectName = sessionAttributes['projectName']

    # If resources already exist, add them all together
    if ("resources" in sessionAttributes):
        sessionResources = sessionAttributes['resources'].split(",")
        resources.extend(sessionResources)

    # Validate resources
    valid = validateResources(resources)
    print(valid)
    sessionAttributesToAppend = {}

    # Set the response message
    validString = listResponseBuilder(valid)
    if "pipeline" in valid and "lambda" not in valid:
        message = f"Adding a pipeline without a lambda is not supported."
    elif valid:
        # Append valid resources to session attributes
        sessionAttributesToAppend = {'resources': ",".join(valid)}

        message = f"I have added {validString} to the project, you can deploy your project with: Deploy Project or add some other resources"
    else:
        message = "I didn't understand. Please restate your command."
    return buildLexResponse(0, message, sessionAttributesToAppend, event)


def appendSessionAttributes(attributes, attributesToAppend):
    attributes.update(attributesToAppend)
    return attributes


# Function to gradually start a conversation
def greetUser(event):

    greeting = "Hi"
    if 'name' in event['sessionAttributes']:
        name = event['sessionAttributes']['name']
        greeting = greeting + " " + name

    message = "{}! I am the SimonSays bot. I can help you with the process " \
    "of creating AWS projects and deploying them. Create a project " \
    "or ask me for help for more information!".format(greeting)

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


def deployProject(event):
    try:
        response = lambdaClient.invoke(FunctionName='SimonSaysDeployer',
                        InvocationType='Event',
                        Payload=json.dumps(event['sessionAttributes']))
    except Exception as e:
        print(e)

    projectName = event['sessionAttributes']['projectName']
    return buildLexResponse(0, f"Deployed {projectName}", {}, event)


if os.environ['DEBUG'] == "True":
    jsonFile = open(sys.argv[1], "r")
    input = jsonFile.read()
    inputDict = json.loads(input)
    lambda_handler(inputDict, None)
