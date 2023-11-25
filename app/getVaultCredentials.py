##connect to Azure Key Vault and get credentials
##return credentials to app.py
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def getSQLVaultCredentials(vault_uri , secret_name):
    credential = DefaultAzureCredential()

    secretclient =  SecretClient(vault_url=vault_uri, credential=credential)

    secret = secretclient.get_secret(secret_name)

    return secret


def getCosmosVaultCredentials(vault_uri, secret_name):
    credential = DefaultAzureCredential()

    secretclient =  SecretClient(vault_url=vault_uri, credential=credential)

    cosmos_secret = secretclient.get_secret(secret_name)

    return cosmos_secret

def getCosmosURI(vault_uri, secret_name):
    credential = DefaultAzureCredential()

    secretclient =  SecretClient(vault_url=vault_uri, credential=credential)

    cosmos_uri = secretclient.get_secret(secret_name)

    return cosmos_uri

def getContainerName(vault_uri, secret_name):
    credential = DefaultAzureCredential()

    secretclient =  SecretClient(vault_url=vault_uri, credential=credential)

    container_name = secretclient.get_secret(secret_name)

    return container_name
