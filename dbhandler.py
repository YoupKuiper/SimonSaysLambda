import boto3

# TODO Change table name from hardcoded to environmentvar
DB_NAME = 'SimonSaysCFNTemplates'
DB_DEBUG_TYPE = 'dbdebug'


class dbhandler:
    '''
    Subroutine for accessing the db table. For DB_DEBUG_TYPE make sure local
    db is running.
    https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SettingUp.html
    '''

    def getDebugDB():
        dynamodb = boto3.resource('dynamodb',
                     endpoint_url='http://localhost:8000')
        table = dynamodb.Table(DB_NAME)
        return table

    def getDB():
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(DB_NAME)
        return table
