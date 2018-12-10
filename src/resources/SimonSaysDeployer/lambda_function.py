from TemplateBuilder import TemplateBuilder
import time
import boto3
from dbhandler import dbhandler

t = TemplateBuilder()
cloudFormationClient = boto3.client('cloudformation')
projTable = dbhandler.getDB("project")


def lambda_handler(event, context):
    resources = event['resources'].split(',')
    projectName = event['projectName']

    if 'vpc' in resources:
        t.addResource('vpc')
        t.addMappings('vpc')
        t.addParameters('vpc')
        t.addOutputs('vpc')
        resources.remove('vpc')
        createStackFromTemplateBody(projectName + "-VPC", projectName, t.getTemplate())
        t.clear()

    for resource in resources:
        t.addResource(resource)
        t.addMappings(resource)
        t.addParameters(resource)
        t.addOutputs(resource)

    createStackFromTemplateBody(projectName, projectName, t.getTemplate())


# Deploy a created project by launching the stack with cloudformation
def deployProject(event):
    projectName = event['projectName']

    # Add project to projects table
    projTable.put_item(Item={"ProjectName": projectName,
                             "resources": t.getTemplate()})

    createStackFromTemplateBody(projectName, t.getTemplate())


def createStackFromTemplateBody(stackName, projectName, templateBody):
    response = cloudFormationClient.create_stack(
        StackName=stackName,
        TemplateBody=str(templateBody),
        Capabilities = ['CAPABILITY_NAMED_IAM'],
        Parameters=[
            {
                'ParameterKey': 'ProjectName',
                'ParameterValue': projectName,
            }
        ]
        )

    response = cloudFormationClient.describe_stacks(StackName=stackName)

    while response['Stacks'][0]['StackStatus'] == "CREATE_IN_PROGRESS":
        time.sleep(10)
        response = cloudFormationClient.describe_stacks(StackName=stackName)
