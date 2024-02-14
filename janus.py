#!/usr/bin/python3
import requests
import boto3
import json
import os


def get_metadata(path: str, parameter: str):
    # Use .format() instead of f-type to support python version before 3.7
    metadata_url = 'http://metadata.google.internal/computeMetadata/v1/{}/{}'.format(path, parameter)
    headers = {'Metadata-Flavor': 'Google'}
    # execute http metadata request
    try:
        meta_request = requests.get(metadata_url, headers=headers)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    if meta_request.ok:
        return meta_request.text
    else:
        raise SystemExit('Compute Engine meta data error')


def get_temp_credentials(aws_role_arn: str, gcp_token_audience: str, session_duration: int):
    instance_name = get_metadata('instance', 'hostname')
    project_id = get_metadata('project', 'project-id')
    project_and_instance_name = '{}.{}'.format(project_id, instance_name)[:64]
    token = get_metadata('instance',
                         'service-accounts/default/identity?format=standard&audience={}'.format(gcp_token_audience))

    sts = boto3.client('sts', aws_access_key_id='', aws_secret_access_key='')

    res = sts.assume_role_with_web_identity(
        RoleArn=aws_role_arn,
        WebIdentityToken=token,
        RoleSessionName=project_and_instance_name,
        DurationSeconds=session_duration
    )

    aws_temporary_credentials = {
        'Version': 1,
        'AccessKeyId': res['Credentials']['AccessKeyId'],
        'SecretAccessKey': res['Credentials']['SecretAccessKey'],
        'SessionToken': res['Credentials']['SessionToken'],
        'Expiration': res['Credentials']['Expiration'].isoformat()
    }

    return aws_temporary_credentials


def get_env_variable(var_name: str):
    var_value = os.getenv(var_name)
    if var_value is None:
        raise RuntimeError("The environment variable '{}' is not set.".format(var_name))
    return var_value


if __name__ == '__main__':
    # Get AWS Role ARN from env
    arn = get_env_variable('AWS_ROLE_ARN')
    # Get GCP Token Audience from env
    audience = get_env_variable('GCP_TOKEN_AUDIENCE')
    # Get AWS session duration from env
    duration = int(os.getenv('AWS_SESSION_DURATION', 3600))

    # Get AWS credentials
    creds = get_temp_credentials(aws_role_arn=arn, gcp_token_audience=audience, session_duration=duration)

    print(json.dumps(creds))
