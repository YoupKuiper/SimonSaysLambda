import boto3

client = boto3.client('dynamodb', region_name='us-east-1')

def handleRequest(event, context):
    echo "aangepast"
    intent_name = intent_request['currentIntent']['name']
    if intent_name == 'createTable':
        return createTable(event, context)
    elif intent_name == 'createDatabase':
        return createDatabase(event, context)

def createTable(event, context):
    response = client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'Artist',
                'AttributeType': 'S'
            },
        ],
        TableName='Youp',
        KeySchema=[
            {
                'AttributeName': 'Artist',
                'KeyType': 'HASH'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

def createDatabase(event, context):
    response = client.create_db_instance(
    DBName='miraBotRelationalDB',
    DBInstanceIdentifier='myFirstInstance',
    AllocatedStorage=123,
    DBInstanceClass='db.m4',
    Engine='mysql',
    MasterUsername='string',
    MasterUserPassword='string',
    DBSecurityGroups=[
        'string',
    ],
    VpcSecurityGroupIds=[
        'string',
    ],
    AvailabilityZone='string',
    DBSubnetGroupName='string',
    PreferredMaintenanceWindow='string',
    DBParameterGroupName='string',
    BackupRetentionPeriod=123,
    PreferredBackupWindow='string',
    Port=123,
    MultiAZ=True|False,
    EngineVersion='string',
    AutoMinorVersionUpgrade=True|False,
    LicenseModel='string',
    Iops=123,
    OptionGroupName='string',
    CharacterSetName='string',
    PubliclyAccessible=True|False,
    Tags=[
        {
            'Key': 'string',
            'Value': 'string'
        },
    ],
    DBClusterIdentifier='string',
    StorageType='string',
    TdeCredentialArn='string',
    TdeCredentialPassword='string',
    StorageEncrypted=True|False,
    KmsKeyId='string',
    Domain='string',
    CopyTagsToSnapshot=True|False,
    MonitoringInterval=123,
    MonitoringRoleArn='string',
    DomainIAMRoleName='string',
    PromotionTier=123,
    Timezone='string',
    EnableIAMDatabaseAuthentication=True|False,
    EnablePerformanceInsights=True|False,
    PerformanceInsightsKMSKeyId='string',
    PerformanceInsightsRetentionPeriod=123,
    EnableCloudwatchLogsExports=[
        'string',
    ],
    ProcessorFeatures=[
        {
            'Name': 'string',
            'Value': 'string'
        },
    ]
)
