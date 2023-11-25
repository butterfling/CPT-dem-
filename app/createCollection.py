import chromadb


##create collection in chromadb
chroma_client = chromadb.PersistentClient(path="chroma.db")
collection = chroma_client.create_collection("HexaDCP")