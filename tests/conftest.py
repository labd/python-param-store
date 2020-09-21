import boto3


def pytest_configure():
    boto3.setup_default_session(region_name="eu-west-1")
