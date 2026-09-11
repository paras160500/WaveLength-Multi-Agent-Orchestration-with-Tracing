# =========================================================================================
#                                     Import/Init Statements
# =========================================================================================

import sqlite3
import requests
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from app.config import settings

# =========================================================================================
#                                        Class Statements
# =========================================================================================

def _build_engine():
    """
        Download the Chinook SQL Script and load into in-memory SQLite DB
    """
    response = requests.get(settings.chinook_sql_url , timeout=30)
    response.raise_for_status()
    sql_script = response.text 

    # check_same_thread = we dont want sql to be like only creation thread can access we want like any thread can access
    connection = sqlite3.connect(":memory:" , check_same_thread=False)
    connection.executescript(sql_script)

    return create_engine(
        "sqlite://",
        creator=lambda : connection,
        poolclass=StaticPool,
        connect_args={"check_same_thread" : False}
    )


# During the lifespan it will call and download the data
_engine = _build_engine()
db = SQLDatabase(_engine)