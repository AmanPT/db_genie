# utils/db_connection.py
from sqlalchemy import create_engine, MetaData

def connect_to_db(uri):
    engine = create_engine(uri)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    return engine, metadata
