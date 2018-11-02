import json
import decimal
from dbhandler import dbhandler

table = dbhandler.getDB("template")


class TemplateBuilder:
    # Class for generating templates with cloudformation resources

        # Create tempBase for resources
    def __init__(self):
        self.__tempBase = {"AWSTemplateFormatVersion": "2010-09-09" ,'Parameters' : {"ProjectName": {"Default": "SvenTestBuild", "Type": "String"}}, 'Resources': {}}

    def clear(self):
        self.__tempBase = {"AWSTemplateFormatVersion": "2010-09-09" ,'Parameters' : {"ProjectName": {"Default": "SvenTestBuild", "Type": "String"}}, 'Resources': {}}

        # Get resources from the database and add to the base
    def addResource(self, type):
        resource = table.get_item(Key={'Id': type})
        item = resource["Item"]["json"]
        itemDict = json.loads(item)
        print("template")
        self.__tempBase['Resources'].update(itemDict)
        print(self.__tempBase)

        # Print json for debug
    def printJSON(self):
        print(json.dumps(self.__tempBase, separators=(',',':'), indent=4, cls=DecimalEncoder))

    def getTemplate(self):
        return (json.dumps(self.__tempBase, separators=(',',':'), indent=4, cls=DecimalEncoder))


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