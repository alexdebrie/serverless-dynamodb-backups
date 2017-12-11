import datetime
import os

# To get updated botocore data files
os.environ['AWS_DATA_PATH'] = '.'

import boto3
import botocore
from botocore.exceptions import ClientError
from botocore.vendored import requests

CLIENT = boto3.client('dynamodb')
TABLE_NAME = os.environ['TABLE_NAME']
SLACK_WEBHOOK = os.environ.get('SLACK_WEBHOOK')
REGION = os.environ.get('AWS_DEFAULT_REGION')
CONSOLE_ENDPOINT = 'https://console.aws.amazon.com/dynamodb/home?region={region}#backups:'.format(region=REGION)


def create_backup(event, context):
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    backup_name = TABLE_NAME + "_" + timestamp
    try:
        resp = CLIENT.create_backup(
            TableName=TABLE_NAME,
            BackupName=backup_name
        )
        message = "\n".join([
            "Created backup for table {table}".format(table=TABLE_NAME),
            "Check your backups <{endpoint}|here>".format(endpoint=CONSOLE_ENDPOINT)
        ])
    except ClientError as e:
        # Error when trying to a backup a table without backups allowed
        if e.response['Error']['Code'] == 'ContinuousBackupsUnavailableException':
            message = "\n".join([
                "*WARNING:* Could not create backup for table {table}".format(table=TABLE_NAME),
                "AWS has not enabled backups for this table. This is not a transient error."
            ])
        # This error was showing up when I used a colon in my backup name. Not very descriptive.
        elif e.response['Error']['Code'] == 'InternalServerError':
            message = "\n".join([
                "*WARNING:* Could not create backup for table {table}".format(table=TABLE_NAME),
                "Error: InternalServerError. This could mean an invalid character in your backup name."
            ])
        else:
            message = "\n".join([
                "*WARNING:* Could not create backup for table {table}".format(table=TABLE_NAME),
                "Error: {msg}".format(msg=e)
            ])
    except Exception as e:
        message = "\n".join([
            "*WARNING:* Could not create backup for table {table}".format(table=TABLE_NAME),
            "Error: {msg}".format(msg=str(e))
        ])
    send_to_slack(message)


def send_to_slack(message):
    if not SLACK_WEBHOOK:
        print('No SLACK_WEBHOOK provided. Not sending a message...')
        return
    data = {"text": message}
    resp = requests.post(SLACK_WEBHOOK, json=data)

    resp.raise_for_status()


if __name__ == "__main__":
    create_backup('', '')
