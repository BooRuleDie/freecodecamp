from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# postgres://<username>:<password>@<ip address or hostname>/<db name>
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.databaseUsername}:{settings.databasePassword}@{settings.databaseHostName}/{settings.databaseName}"

# it's the same as creating a connection in traditional model
Engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# trying to make a connection to the database
# if successful break the loop 
# while(True):
#     try:
#         conn = psycopg2.connect(host="", dbname="", user="", password="", cursor_factory=RealDictCursor) 
#         cursor = conn.cursor()
#         break
#     except Exception as error:
#         print(f"Connection Failed.\nError: {error}")
#         sleep(3)
