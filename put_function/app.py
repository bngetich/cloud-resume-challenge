import json
import boto3
import decimal
from botocore.exceptions import ClientError

counter_table = boto3.resource('dynamodb').Table('countertable')

def lambda_handler(event, context):
    
    try:
        response = counter_table.update_item(
            Key={'siteviews': 'view_counter'},
            ExpressionAttributeValues={':inc': decimal.Decimal(1)},
            UpdateExpression="ADD counter_value :inc"
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return {
            "headers": {
                "Access-Control-Allow-Origin":  "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*",
            },
            "statusCode": 200
        }
