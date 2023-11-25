first -> az login -> aquires Azure default credential()
then fetch the database credentials stored in Azure key vault
connect to the database to access company data 
connect to metadata database to access the customer metadata

create a message queue filteting out initially for batch processing 
create six different SQL tables (grouping) based on metadata feilds

create a RAG