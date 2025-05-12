import boto3

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id='AKIAUGQBRYZHDGHNDRFB',
    aws_secret_access_key='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',
    region_name='ap-northeast-2'
)

users_table = dynamodb.Table('Users')