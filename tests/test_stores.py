import boto3
import moto

from param_store import EC2ParameterStore, FileParameterStore


@moto.mock_ssm
def test_ec2_parameter_store():
    region_name = "eu-west-1"
    ssm = boto3.client("ssm", region_name=region_name)
    ssm.put_parameter(Name="key", Value="hoi", Type="SecureString")
    ssm.put_parameter(Name="second-key", Value="doei", Type="String")

    store = EC2ParameterStore(aws_config={"region_name": region_name})
    result = store.load_values(["key", "second-key", "non-existing-key"])
    assert result == {"key": "hoi", "second-key": "doei"}


@moto.mock_ssm
def test_ec2_parameter_store_many():
    region_name = "eu-west-1"
    data = {
        "/path/key/a": "a",
        "/path/key/b": "b",
        "/path/key/c": "c",
        "/path/key/d": "d",
        "/path/key/e": "e",
        "/path/key/f": "f",
        "/path/key/g": "g",
        "/path/key/h": "h",
        "/path/key/i": "i",
        "/path/key/j": "j",
        "/path/key/k": "k",
    }
    ssm = boto3.client("ssm", region_name=region_name)
    for key, value in data.items():
        ssm.put_parameter(Name=key, Value=value, Type="String")

    store = EC2ParameterStore(aws_config={"region_name": region_name})
    result = store.load_values(list(data.keys()))
    assert result == data


@moto.mock_ssm
def test_ec2_parameter_store_different_parameters():
    right_region_name = "eu-west-1"
    key_wanted = "key-eu-weast-1"
    ssm = boto3.client("ssm", region_name=right_region_name)
    ssm.put_parameter(Name=key_wanted, Value="hoi", Type="SecureString")

    store = EC2ParameterStore(aws_config={"region_name": "us-east-1"})
    result = store.load_values([key_wanted])
    assert key_wanted not in result

    store = EC2ParameterStore(aws_config={"region_name": right_region_name})
    result = store.load_values([key_wanted])
    assert key_wanted in result
    assert result == {key_wanted: "hoi"}


def test_file_parameter_store(tmpdir):
    secret_path = tmpdir.mkdir("secrets")
    secret_path.join("key").write("hoi")
    secret_path.join("second-key").write("doei")

    store = FileParameterStore(path=secret_path.realpath())
    result = store.load_values(["key", "second-key", "non-existent-key"])
    assert result == {"key": "hoi", "second-key": "doei"}, result


def test_file_parameter_store_invalid_path(tmpdir):
    path = tmpdir.mkdir("secrets")
    path.join("key").write("hoi")

    store = FileParameterStore(path.join("invalid").realpath())
    result = store.load_values(["key"])
    assert result == {}
