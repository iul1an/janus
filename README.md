# Janus

Janus is a python script that allows you to assume role (retrieve temporary AWS IAM token) from Google Cloud using a service account.

## Installation

Please visit [this blog post](https://www.doit-intl.com/assume-an-aws-role-from-a-google-cloud-without-using-iam-keys/) for the installation.

## Usage

```shell
$ export AWS_ROLE_ARN=arn:aws:iam::123456789:role/gcp-to-aws
$ export GCP_TOKEN_AUDIENCE=foo # this value may be used as a condition in the AWS assume role policy
$ export AWS_SESSION_DURATION=7200 # optional, defaults to 3600s (1h), must have value less than or equal to 43200 (12h)
$ python janus.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
