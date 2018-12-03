import json
import decimal
from dbhandler import dbhandler

table = dbhandler.getDB("template")


class TemplateBuilder:
    # Class for generating templates with cloudformation resources

        # Create tempBase for resources
    def __init__(self):
        self.__tempBase = {}

    def clear(self):
        self.__tempBase = {}

        # Get resources from the database and add to the base
    def addResource(self, type):
        resource = table.get_item(Key={'Id': type})
        item = resource["Item"]["json-resources"]
        itemDict = json.loads(item)
        self.__tempBase.update({"Resources": itemDict})

        # Get parameters from the database and add to the base
    def addParameters(self, type):
        parameter = table.get_item(Key={'Id': type})
        item = parameter["Item"]["json-parameters"]
        itemDict = json.loads(item)
        self.__tempBase.update({"Parameters": itemDict})

        # Get mappings from the database and add to the base
    def addMappings(self, type):
        mappings = table.get_item(Key={'Id': type})
        item = mappings["Item"]["json-mappings"]
        itemDict = json.loads(item)
        self.__tempBase.update({"Mappings": itemDict})

    def addExports(self, type):
        exports = table.get_item(Key={'Id': type})
        item = exports["Item"]["json-exports"]
        itemDict = json.loads(item)
        self.__tempBase.update({"exports": itemDict})

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
