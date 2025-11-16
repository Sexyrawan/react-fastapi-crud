# db connection 
# sql query 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_url = "postgresql://postgres:rahul@localhost:5432/telusko"
engine = create_engine(db_url)
sessionlocal = sessionmaker(autocommit = False , autoflush=False, bind=engine)

session = sessionmaker(autocommit=False, autoflush=False , bind=engine)