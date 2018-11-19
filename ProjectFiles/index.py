import json


def lambda_handler(event, context):
    message = {"person": {"name": "sven"}}

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Origin': '*',
            'Allow': 'GET, OPTIONS, POST',
            'Access-Control-Allow-Methods': 'GET, OPTIONS, POST',
            'Access-Control-Allow-Headers': '*'
        },
        'body': json.dumps(message, sort_keys=True, indent=4, separators=(',', ': '))
        }
