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
