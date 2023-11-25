from getVaultCredentials import getSQLVaultCredentials, getCosmosVaultCredentials, getCosmosURI, getContainerName
from authenticateDatabase import connect_to_sql_database, connect_to_cosmos_db

from applicationConfig import app_config
import subprocess


queue_vault_url = app_config.get('vault_uri', '')


config_file_path = 'config.txt'  

def read_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key.strip()] = value.strip().strip('"')
    return config

config = read_config(config_file_path)

##Read config file
vault_url = config.get('vault_url', '')
database_secret_name = config.get('database_secret_name', '')
metadata_secret_name = config.get('metadata_secret_name', '')
metadata_uri = config.get('metadata_uri', '')
container_name = config.get('container_name', '')



##Get credentials from Azure Key Vault and Authenticate Admin Database
admin_sql_credentials = getSQLVaultCredentials(vault_url, database_secret_name)
admin_metadata_credentials = getCosmosVaultCredentials(vault_url, metadata_secret_name)
admin_metadata_uri = getCosmosURI(vault_url, metadata_uri).value
container_name = getContainerName(vault_url, container_name)

conn = connect_to_sql_database(vault_url, database_secret_name)
cursor1 = conn.cursor()

client =connect_to_cosmos_db(vault_url, metadata_uri, metadata_secret_name)

##Build a batch process to enqueue first filtering process
subprocess.run(["python", "appEnqueue.py"])

##Process batch data and start second filtering process
subprocess.run(["python", "batchProcess.py"])

##Create SQL Tables according to the metadata feilds 
subprocess.run(["python", "dataRecords.py"])

subprocess.run(["python", "textToSpeech.py"])