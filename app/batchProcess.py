from appEnqueue import queue_client, isEncrypted
from authenticateDatabase import connect_to_sql_database
import json



connect = connect_to_sql_database("https://cptdatabasecredentials.vault.azure.net/","dbadmin")

cursor = connect.cursor()


def consentGiven(cursor, customer_id):
    fields_to_check = ["[Email]", "[Social-Security-Number]", "[Financial-Information]"]

    for field in fields_to_check:

        if not isEncrypted(cursor,customer_id, field):

            consentQuery = "SELECT [Name], [Phone Number], [Email], [Social-Security-Number], [Financial-Information] FROM CustomersInformation WHERE [Customer ID] = ?"
            cursor.execute(consentQuery, customer_id)
            record = cursor.fetchone()

            if record:

                insertQuery = f"INSERT INTO consentGiven ([Customer ID], [Name], [Phone Number], [Email], [Social-Security-Number], [Financial-Information]) VALUES (?, ?, ?, ?, ?, ?)"
                cursor.execute(insertQuery, (customer_id, record[0], record[1], record[2], record[3], record[4]))
                connect.commit()



def legalObligation(cursor, customer_id):

    fields_to_check = ["[Social-Security-Number]", "[Financial-Information]"]

    for field in fields_to_check:
            
            if not isEncrypted(cursor,customer_id, field):
    
                consentQuery = "SELECT [Name], [Phone Number], [Email], [Social-Security-Number], [Financial-Information] FROM CustomersInformation WHERE [Customer ID] = ?"
                cursor.execute(consentQuery, customer_id)
                record = cursor.fetchone()
    
                if record:
    
                    insertQuery = f"INSERT INTO consentGiven ([Customer ID], [Name], [Phone Number], [Email], [Social-Security-Number], [Financial-Information]) VALUES (?, ?, ?, ?, ?, ?)"
                    cursor.execute(insertQuery, (customer_id, record[0], record[1], record[2], record[3], record[4]))
                    connect.commit()

def process_batch_queue():

    # Receive messages from the queue
    messages = queue_client.receive_messages(messages_per_page=5)
    for msg_batch in messages.by_page():
        for msg in msg_batch:
            # Process the messages
            content = json.loads(msg.content)
            print(content)
            
            if not content['consentGiven']:
                consentGiven(cursor, content['customer_id'])
            
            elif not content['legalObligation']:
                legalObligation(cursor, content['customer_id'])
    
            
            queue_client.delete_message(msg)

process_batch_queue()