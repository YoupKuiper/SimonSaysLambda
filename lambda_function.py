import boto3
from TemplateBuilder import TemplateBuilder

client = boto3.client('cloudformation')
t = TemplateBuilder()


def lambda_handler(event, context):
    currentIntent = event['currentIntent']['name']
    if currentIntent == "CreateProject":
        return createProject(event)
    elif currentIntent == "AddResources":
        return buildTemplate(event)
    # elif currentIntent == "AddDefaultVPC":
    #     return addDefaultVPC(event)
    # elif currentIntent == "AddCustomVPC":
    #     return addCustomVPC(event)
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
    projectName = event['sessionAttributes']['projectName']
    for resourceSlot in event['currentIntent']['slots']:
        resource = event['currentIntent']['slots'][resourceSlot]
        t.addResource(resource)
    createStackFromTemplateBody(projectName, t)
    message = f"The resources were added to project {projectName}."
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
        TemplateBody=templateBody.printJSON())

    print(response)


    # def addCustomVPC(event):
    #     amountOfPublicSubnets = event['currentIntent']['slots']['AmountOfPublicSubnets']
    #     amountOfPrivateSubnets = event['currentIntent']['slots']['AmountOfPrivateSubnets']
    #
    #     sessionAttributesToAppend = {
    #         "VPC": "custom",
    #         "amountOfPublicSubnets": amountOfPublicSubnets,
    #         "amountOfPrivateSubnets": amountOfPrivateSubnets
    #     }
    #     projectName = event['sessionAttributes']['projectName']
    #     template = Template()
    #     template.addVPC()
    #     template.addSubnet(int(amountOfPrivateSubnets) + int(amountOfPublicSubnets), "VPC")
    #     print(str(template.printJSON()))
    #     createStackFromTemplateBody(projectName, template)
    #     message = f"A custom VPC with {amountOfPublicSubnets} public subnets and {amountOfPrivateSubnets} private subnets has been added to project {projectName}"
    #
    #     return buildLexResponse(1, message, sessionAttributesToAppend, event)


    # def addDefaultVPC(event):
    #     projectName = event['sessionAttributes']['projectName']
    #     message = f"The default VPC has been added to project {projectName}."
    #     sessionAttributesToAppend = {"VPC": "default"}
    #     templateURL = "https://s3-eu-west-1.amazonaws.com/demobucketsimonsays/demoTemplate.json"
    #     createStackFromURL(projectName, templateURL)
    #     return buildLexResponse(1, message, sessionAttributesToAppend, event)
