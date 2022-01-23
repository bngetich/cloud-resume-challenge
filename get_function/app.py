import json
import boto3
from botocore.exceptions import ClientError
import decimal

counter_table = boto3.resource("dynamodb").Table("countertable")


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def lambda_handler(event, context):

    try:
        item = counter_table.get_item(Key={"siteviews": "view_counter"})
        count_views = item["Item"]["counter_value"]
    except ClientError as e:
        print(e.response["Error"]["Message"])
    else:
        return {
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*",
            },
            "statusCode": 200,
            "body": json.dumps(
                {
                    "count": count_views,
                },
                indent=4,
                cls=DecimalEncoder,
            )
        }
