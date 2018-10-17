import sys
import json
import boto3
from dbhandler import dbhandler
# Use this script to add templates for resources to the database and add slottypes to lex

# Read file from json and parse to dict
jsonFile = open(sys.argv[1], "r")
input = jsonFile.read()

# Parse json to dict
inputDict = json.loads(input)

# Get the type of resource
type = sys.argv[2]

# Get dynamodb table
table = dbhandler.getDB()

# Put the resource template in the db if it doesnt exist already
response = table.put_item(
    Item={"Id": type, "json": inputDict},
    ConditionExpression='attribute_not_exists(Id)'
    )

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

print(enumerationValues)

newSlotType = client.put_slot_type(
    name='Resources',
    description='test',
    enumerationValues=enumerationValues,
    checksum='',
    valueSelectionStrategy='ORIGINAL_VALUE',
    createVersion=False
)


