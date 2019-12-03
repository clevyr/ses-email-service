import json
import os
import time

import boto3

SES = boto3.client('ses')
SQS = boto3.client('sqs')
dynamodb = boto3.client('dynamodb')

SES_RATE_LIMIT = int(os.getenv('AWS_SES_RATE_LIMIT', '10'))
QUEUE_URL = os.getenv('AWS_SQS_URL', '')
USE_BLACKLIST = os.getenv('USE_BLACKLIST', 'false').lower() == True

# You can only pull 10 messages at a time max
MAX_SQS_MESSAGES = SES_RATE_LIMIT if SES_RATE_LIMIT <= 10 else 10


def removeBlacklist(email_addresses):
    new_addresses = []
    for email in email_addresses:
        item = dynamodb.get_item(
            Key={
                'email': {
                    'S': email,
                },
            },
            TableName='ses_blacklist',
        )
        if 'Item' in item.keys():
            print(f'Removing {email} from the sender list due to being blacklisted')
        else:
            new_addresses.append(email)
    return new_addresses


def main():
    print('Listening for emails')
    while True:
        response = SQS.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=MAX_SQS_MESSAGES,
            WaitTimeSeconds=0
        )

        if response and 'Messages' in response and len(response['Messages']) > 0:
            for message in response['Messages']:
                email = json.loads(message['Body'])
                if email is not None:
                    if USE_BLACKLIST:
                        # Filter out blacklisted email addresses
                        email['Destination']['ToAddresses'] = removeBlacklist(email['Destination']['ToAddresses'])

                    SES.send_email(**email)
                    SQS.delete_message(
                        QueueUrl=QUEUE_URL,
                        ReceiptHandle=message['ReceiptHandle']
                    )
                    if 'Destination' not in email:
                        print('Email doesn\'t have destination')
                    else:
                        dest = email['Destination']['ToAddresses']
                        print(f'Email sent to {dest}')
        time.sleep(2)


if __name__ == "__main__":
    main()
