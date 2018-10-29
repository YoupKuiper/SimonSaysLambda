import boto3
import os

# TODO Change table name from hardcoded to environmentvar
TEMPLATE_DB_NAME = 'SimonSaysCFNTemplates'
PROJECT_DB_NAME = 'SimonSaysProjects'
DB_DEBUG_TYPE = 'dbdebug'

class dbhandler:
    '''
    Subroutine for accessing the db table. For DB_DEBUG_TYPE make sure local
    db is running.
    https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SettingUp.html
    '''

    def getDB(type):
        msg = ""
        if os.getenv("DEBUG") == "True":
            dynamodb = boto3.resource('dynamodb',
                         endpoint_url='http://localhost:8000')
            msg = msg + "[Debug databate connection]"
        else:
            dynamodb = boto3.resource('dynamodb')
            msg = msg + "[Prod database connection]"

        if type == "template":
            table = dynamodb.Table(TEMPLATE_DB_NAME)
            msg = msg + "[Attached template database]"
            print(msg)
            return table
        else:
            table = dynamodb.Table(PROJECT_DB_NAME)
            msg = msg + "[Attached project database]"
            print(msg)
            return table
