# SES Email Service

This service is used to help with clients who need a large amount of emails sent via SES and need to deal with rate limiting.

There are two services within this repo, the SES Email Service to be run as a Docker container, and the Email Blacklist service that runs in Lambda and listens to SNS for email bounce or complaint notifications, and adds them to a global blacklist.

## Service Environment Variables

|       Environment Variable        |                                                                       Details                                                                       |                          Example                          |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| `AWS_ACCESS_KEY_ID`               | Specifies an AWS access key associated with an IAM user or role.                                                                                    | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`                |
| `AWS_SECRET_ACCESS_KEY`           | Specifies the secret key associated with the access key. This is essentially the "password" for the access key.                                     | `AKIAIOSFODNN7EXAMPLE`                                    |
| `AWS_DEFAULT_REGION`              | Specifies the AWS Region to send the request to.                                                                                                    | `us-east-1`                                               |
| `AWS_SQS_URL`                     | Specifies the SQS queue where emails are sent                                                                                                       | `https://sqs.us-east-2.amazonaws.com/683774710813/emails` |
| `USE_BLACKLIST`                   | Whether to use the Clevyr email recipient blacklist                                                                                                 | `true`                                                    |
| `BLACKLIST_AWS_ACCESS_KEY_ID`     | Specifies an AWS access key associated with an IAM user or role, used to access the shared blacklist                                                | `true`                                                    |
| `BLACKLIST_AWS_SECRET_ACCESS_KEY` | Specifies the secret key associated with the access key. This is essentially the "password" for the access key. Used to access the shared blacklist | `true`                                                    |
| `BLACKLIST_AWS_DEFAULT_REGION`    | Specifies the AWS Region to send the request to. Used to access the shared blacklist                                                                | `true`                                                    |

## Lambda Environment Variables

| Environment Variable |                             Details                             |              Example               |
| -------------------- | --------------------------------------------------------------- | ---------------------------------- |
| `SES_REGION`         | The region that SES is working in                               | `us-east-1`                        |
| `EMAIL_FROM`         | The email address to send emails from                           | `backups@domain.com`               |
| `EMAIL_TO`           | The list of email addresses to send to, separated by semicolons | `user@domain.com;user1@domain.com` |

## IAM Roles

Here are the permissions required to run the Email Blacklist Lambda

### Email Blacklist Lambda

Here are the permissions required to run the Email Blacklist Lambda

#### Email Blacklist Policy

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ses:SendEmail",
                "ses:SendRawEmail"
            ],
            "Resource": [
                "arn:aws:ses:<REGION>:<ACCOUNT_ID>:identity/<SES_DOMAIN>"
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "sns:ConfirmSubscription",
                "sns:Subscribe",
                "sns:Unsubscribe"
            ],
            "Resource": [
                "arn:aws:sns:<REGION>:<ACCOUNT_ID>:<SNS_TOPIC_NAME>"
            ]
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem"
            ],
            "Resource": "arn:aws:dynamodb:<REGION>:<ACCOUNT_ID>:table/<DYNAMODB_TABLE_NAME>"
        }
    ]
}
```

#### Email Blacklist Trust Relationship

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    },
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "sns.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

### Email Blacklist DynamoDB Access

Here are the permissions required to access the Email Blacklist from the SES Service (BLACKLIST_AWS_ACCESS_KEY_ID and adjacent environment variables)

#### Email Blacklist DynamoDB Policy

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "dynamodb:GetItem",
            "Resource": "arn:aws:dynamodb:<REGION>:<ACCOUNT_ID>:table/<TABLE_NAME>"
        }
    ]
}
```
