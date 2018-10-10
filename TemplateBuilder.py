import json
import boto3
import decimal

DB_NAME = 'SimonSaysCFNTemplates'

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

# TODO Change table hardcoded to environmentvar
table = dynamodb.Table(DB_NAME)

# Class for generating templates with cloudformation resources


class TemplateBuilder:

        # Create tempBase for resources
    def __init__(self):
        self.__tempBase = {'Resources': {}}

        # Get resources from the database and add to the base
    def addResource(self, type):
        resource = table.get_item(Key={'Type': type})
        self.__tempBase['Resources'].update(resource)

        # Print json for debug
    def printJSON(self):
        resources = {"Resources": self.__tempBase}
        return json.dumps(resources, cls=DecimalEncoder)


class DecimalEncoder(json.JSONEncoder):
    # Class to fix the boto3 to JSON problem
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
