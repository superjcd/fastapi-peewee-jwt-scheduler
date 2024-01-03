from fastapi import Depends
from app.providers import database
from app.providers.database import reset_db_state

def get_db(db_state=Depends(reset_db_state)):
    try:
        database.db.connect()
        yield
    finally:
        if not database.db.is_closed():
            database.db.close()