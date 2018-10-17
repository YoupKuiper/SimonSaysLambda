# Use this script to add templates for resources to the database and add slottypes to lex
import sys
import json
import boto3
from dbhandler import dbhandler

# Get dynamodb table
table = dbhandler.getDB("template")

# Read file from json and parse to dict
jsonFile = open(sys.argv[1], "r")
input = jsonFile.read()
inputDict = json.loads(input)

# Get the type of resource
type = sys.argv[2]

# Put the template in the table
response = table.put_item(Item={"Type": type, "json": inputDict})
print(response)
# Add type to lex slotTypes

# Get the lex client
client = boto3.client('lex-models')

response = client.get_slot_type(
    name='Resources',
    version='$LATEST'
)
name = response['name']
elem = {'value':type}
enumerationValues = response['enumerationValues']
enumerationValues.append(elem)


response = client.put_slot_type(
    name=name,
    description='test',
    enumerationValues=enumerationValues,
    checksum='',
    valueSelectionStrategy='ORIGINAL_VALUE',
    createVersion=False
)

# print(response)
