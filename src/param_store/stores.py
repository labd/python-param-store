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


class AzureVaultConfigurationException(Exception):
    pass


class AzureVaultParameterStore(BaseStore):

    def __init__(self):
        from azure.keyvault import KeyVaultClient, KeyVaultAuthentication
        from os import getenv

        self.vault_id = getenv("AZURE_VAULT_ID", None)
        self.tenant_id = getenv("AZURE_TENANT_ID", None)

        self.app_id = getenv("AZURE_APP_ID", None)
        self.client_id = getenv("AZURE_CLIENT_ID", None)
        self.secret = getenv("AZURE_SECRET", None)

        if self.app_id:
            import adal

            # create an adal authentication context
            auth_context = adal.AuthenticationContext(
                'https://login.microsoftonline.com/%s' % self.tenant_id)

            def auth_callback(server, resource, scope):
                user_code_info = auth_context.acquire_user_code(resource, self.app_id)

                token = auth_context.acquire_token_with_device_code(resource=resource,
                                                                    client_id=self.app_id,
                                                                    user_code_info=user_code_info)
                return token['token_type'], token['access_token']
        elif self.client_id and self.secret:
            from azure.common.credentials import ServicePrincipalCredentials

            def auth_callback(server, resource, scope):
                credentials = ServicePrincipalCredentials(
                    client_id=self.client_id,
                    secret=self.secret,
                    tenant=self.tenant_id,
                    resource="https://vault.azure.net"
                )
                token = credentials.token
                return token['token_type'], token['access_token']
        else:
            raise AzureVaultConfigurationException("Either set AZURE_APP_ID or "
                                                   "(AZURE_CLIENT_ID and AZURE_SECRET)")

        self.client = KeyVaultClient(KeyVaultAuthentication(auth_callback))

    def load_values(self, items):
        from azure.keyvault.models import KeyVaultErrorException
        from azure.keyvault import KeyVaultId

        if not items or not self.vault_id:
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
