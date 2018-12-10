import sys
import json
import boto3
import subprocess
from dbhandler import dbhandler
# Use this script to add templates for resources to the database and add slottypes to lex
# Pass the filepath as the first parameter and the slot/database name as the second

# Read file from json and parse to dict
jsonFile = open(sys.argv[1], "r")
input = jsonFile.read()

# Parse json to dict
inputDict = json.loads(input)

# Get the type of resource
type = sys.argv[2]

# Get dynamodb table
table = dbhandler.getDB("template")

if 'Mappings' not in input:
    inputDict.update({"Mappings": {}})
if 'Parameters' not in input:
    inputDict.update({"Parameters": {}})
if 'Outputs' not in input:
    inputDict.update({"Outputs": {}})

resources = json.dumps(inputDict["Resources"])
Mappings = json.dumps(inputDict["Mappings"])
Parameters = json.dumps(inputDict["Parameters"])
Outputs = json.dumps(inputDict["Outputs"])

subprocess.call("aws cloudformation validate-template --template-body file:///" + sys.argv[1], shell=True)

# Put the resource template in the db if it doesnt exist already
try:
    response = table.put_item(
        Item={"Id": type, "json": input, "json-resources": resources, "json-mappings": Mappings, "json-parameters": Parameters, "json-outputs": Outputs}
        )
except:
    print("Resource already exists")

response = table.scan()

listOfResources = []
for item in response['Items']:
    listOfResources.append(item["Id"])

print(listOfResources)


# Get the lex client
client = boto3.client('lex-models')

enumerationValues = []
for resource in listOfResources:
    enumerationValue = {'value': resource}
    enumerationValues.append(enumerationValue)

newSlotType = client.put_slot_type(
    name='Resources',
    description='test',
    enumerationValues=enumerationValues,
    checksum='',
    valueSelectionStrategy='TOP_RESOLUTION',
    createVersion=False
)
