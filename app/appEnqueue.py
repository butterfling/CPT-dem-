from azure.storage.queue import QueueServiceClient
from azure.identity import DefaultAzureCredential
from authenticateDatabase import connect_to_sql_database, connect_to_cosmos_db
from getVaultCredentials import getContainerName
import json
# from app import vaulturl , secretname , metadata_secret_name , metadata_uri , container_name, database_secret_name 

databaseName = "democpt"

container  = connect_to_cosmos_db("https://cptdatabasecredentials.vault.azure.net/", "uri","democpt").get_database_client(databaseName).get_container_client(databaseName)

account_url = "https://saahilcptgroupaac8.queue.core.windows.net"  ##Plugin queue deployed on Azure
credential = DefaultAzureCredential()

queue_name = "demobatchqueue"

queue_service_client = QueueServiceClient(account_url=account_url, credential=credential)

conn = connect_to_sql_database("https://cptdatabasecredentials.vault.azure.net/", "dbadmin")

# Create a QueueClient instance
queue_client = queue_service_client.get_queue_client(queue_name)

cursor1 = conn.cursor()


def check_gdpr_compliance(metadata):
    # Define your GDPR violation criteria here
    return not metadata.get("consentGiven", True) or \
           not metadata.get("legalObligation", True) or \
           not metadata.get("vitalInterests", True)


def isEncrypted(cursor,customer_id, field_name):

    query = f"SELECT {field_name} FROM CustomersInformation WHERE [Customer ID] = ?"
    cursor.execute(query, customer_id)
    field_val = cursor.fetchone()[0]

    return field_val.startswith("b'gAAA")

def insertQueue():
    query = "SELECT * FROM c"
    for item in container.query_items(query=query, enable_cross_partition_query=True):
        if check_gdpr_compliance(item):

            content = {
                "customer_id": item['customer_id'],
                "consentGiven": item['consentGiven'],
                "contractualNecessity": item['contractualNecessity'],
                "legalObligation": item['legalObligation'],
                "vitaleInterests": item['vitalInterests'],
                "publicInterest": item['publicInterest'],
            }
            # Create a message
            message = json.dumps(content)
            queue_client.send_message(message)
    

insertQueue()