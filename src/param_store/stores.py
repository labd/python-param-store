from itertools import islice

__all__ = [
    'EC2ParameterStore',
    'AzureVaultParameterStore',
]


class BaseStore(object):

    def load_values(self, items):
        raise NotImplementedError()


class EC2ParameterStore(BaseStore):

    def __init__(self):
        import boto3

        self.client = boto3.client('ssm')

    def load_values(self, items):
        """Load the parameters from the AWS Parameter Store

        :parameter items: list with keys
        :rtype: dict

        """
        if not items:
            return {}

        def chunk(it, size):
            it = iter(it)
            return iter(lambda: tuple(islice(it, size)), ())

        iteritems = chunk(items, 10)
        result = {}
        for items in iteritems:
            data = self.client.get_parameters(
                Names=items,
                WithDecryption=True)

            for parameter in data['Parameters']:
                key = parameter['Name']
                value = parameter['Value']
                result[key] = value
        return result


class AzureVaultParameterStore(BaseStore):

    def __init__(self):
        import adal
        from azure.keyvault import KeyVaultClient, KeyVaultAuthentication
        from os import getenv

        self.vault_id = getenv("AZURE_VAULT_ID")
        self.client_id = getenv("AZURE_APP_ID")
        self.tenant_id = getenv("AZURE_TENANT_ID")

        # create an adal authentication context
        auth_context = adal.AuthenticationContext(
            'https://login.microsoftonline.com/%s' % self.tenant_id)

        def auth_callback(server, resource, scope):
            user_code_info = auth_context.acquire_user_code(resource, self.client_id)

            token = auth_context.acquire_token_with_device_code(resource=resource,
                                                                client_id=self.client_id,
                                                                user_code_info=user_code_info)
            return token['token_type'], token['access_token']

        self.client = KeyVaultClient(KeyVaultAuthentication(auth_callback))

    def load_values(self, items):
        from azure.keyvault.models import KeyVaultErrorException
        from azure.keyvault import KeyVaultId

        if not items:
            return {}

        result = {}
        for key in items:
            try:
                data = self.client.get_secret("https://%s.vault.azure.net/" % self.vault_id,
                                              key, KeyVaultId.version_none)
            except KeyVaultErrorException:
                continue

            result[key] = data.value

        return result
