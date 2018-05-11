import boto3
import moto

from param_store import EC2ParameterStore


@moto.mock_ssm
def test_ec2_parameter_store():
    ssm = boto3.client('ssm')
    ssm.put_parameter(Name='key', Value='hoi', Type='SecureString')
    ssm.put_parameter(Name='second-key', Value='doei', Type='String')

    store = EC2ParameterStore()
    result = store.load_values(['key', 'second-key', 'non-existing-key'])
    assert result == {
        'key': 'hoi',
        'second-key': 'doei',
    }


@moto.mock_ssm
def test_ec2_parameter_store_many():
    data = {
        '/path/key/a': 'a',
        '/path/key/b': 'b',
        '/path/key/c': 'c',
        '/path/key/d': 'd',
        '/path/key/e': 'e',
        '/path/key/f': 'f',
        '/path/key/g': 'g',
        '/path/key/h': 'h',
        '/path/key/i': 'i',
        '/path/key/j': 'j',
        '/path/key/k': 'k',
    }
    ssm = boto3.client('ssm')
    for key, value in data.items():
        ssm.put_parameter(Name=key, Value=value, Type='String')

    store = EC2ParameterStore()
    result = store.load_values(list(data.keys()))
    assert result == data
