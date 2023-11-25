import pyodbc
from azure.cosmos import CosmosClient, PartitionKey
from getVaultCredentials import getSQLVaultCredentials, getCosmosVaultCredentials, getCosmosURI

def connect_to_sql_database(vault_url, secret_name):
    # Get credentials from Azure Key Vault for SQL Database
    secret = getSQLVaultCredentials(vault_url, secret_name)

    uid = secret.name  # Username
    pwd = secret.value # Password

    # Construct the connection string
    conn_str = (
        "Driver={ODBC Driver 18 for SQL Server};"
        "Server=tcp:democustomerserver.database.windows.net,1433;"
        "Database=demoCustomerDatabase;"
        f"Uid={uid};"
        f"Pwd={pwd};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=90;"
    )

    # Establish the connection to SQL Database
    conn = pyodbc.connect(conn_str)
    return conn

def connect_to_cosmos_db(vault_url, secret_name, metadata_secret_name):
    # Get credentials and URI from Azure Key Vault for Cosmos DB
    cosmos_secret = getCosmosVaultCredentials(vault_url, metadata_secret_name)
    cosmos_uri = getCosmosURI(vault_url, secret_name)

    uri = cosmos_uri.value
    primary_key = cosmos_secret.value

    # Create a Cosmos client
    client = CosmosClient(uri, credential=primary_key)
    return client

