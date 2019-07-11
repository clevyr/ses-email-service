# SES Email Service

This service is used to help with clients who need a large amount of emails sent via SES and need to deal with rate limiting.

## Environment Variables

|  Environment Variable   |                                                     Details                                                     |                          Example                          |
| ----------------------- | --------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| `AWS_ACCESS_KEY_ID`     | Specifies an AWS access key associated with an IAM user or role.                                                | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`                |
| `AWS_SECRET_ACCESS_KEY` | Specifies the secret key associated with the access key. This is essentially the "password" for the access key. | `AKIAIOSFODNN7EXAMPLE`                                    |
| `AWS_DEFAULT_REGION`    | Specifies the AWS Region to send the request to.                                                                | `us-east-1`                                               |
| `AWS_SES_RATE_LIMIT`    | Specifies the SES messages per second rate limit                                                                | `14`                                                      |
| `AWS_SQS_URL`           | Specifies the SQS queue where emails are sent                                                                   | `https://sqs.us-east-2.amazonaws.com/683774710813/emails` |
