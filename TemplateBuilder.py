import json
import decimal
from dbhandler import dbhandler

# using local debug db. Use getDB for online developmentDB
table = dbhandler.getDB()


class TemplateBuilder:
    # Class for generating templates with cloudformation resources

        # Create tempBase for resources
    def __init__(self):
        self.__tempBase = {'Resources': {}}

        # Get resources from the database and add to the base
    def addResource(self, type):
        resource = table.get_item(Key={'Type': type})
        item = resource["Item"]["json"]
        item = json.dumps(item, separators=(',',':'), indent=4, cls=DecimalEncoder)
        self.__tempBase['Resources'].update(item)

        # Print json for debug
    def printJSON(self):
        print(json.dumps(self.__tempBase, separators=(',',':'), indent=4, cls=DecimalEncoder))

    def getTemplate(self):
        return self.__tempBase


class DecimalEncoder(json.JSONEncoder):
    # Class to fix the boto3 to JSON problem
    # Converts decimal dynamodb val to int
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
