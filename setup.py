import os
from sqlalchemy import create_engine, Column, Integer, String, Index, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def get_database_url():
    database_type = os.getenv('DATABASE_TYPE', 'sqlite')    
    database_url = os.getenv('DATABASE_URL', 'properties.db')
    database_username = os.getenv('DATABASE_USERNAME', None)
    database_password = os.getenv('DATABASE_PASSWORD', None)
    database_host = os.getenv('DATABASE_HOST', None)
    database_port = os.getenv('DATABASE_PORT', None)
    database_name = os.getenv('DATABASE_NAME', None)

    if database_type == 'sqlite':
        return f'sqlite:///{database_url}'
    elif database_type == 'mysql':
        return f'mysql+mysqlconnector://{database_username}:{database_password}@{database_host}:{database_port or 3306}/{database_name}'
    elif database_type == 'postgresql':
        return f'postgresql+psycopg2://{database_username}:{database_password}@{database_host}:{database_port or 5432}/{database_name}'
    else:
        raise ValueError(f"Unsupported database type: {database_type}")


database_url = get_database_url()

# Create the SQLAlchemy engine
engine = create_engine(database_url, echo=True)

# Create a base class for the declarative models
Base = declarative_base()

# Define the properties table as a model
class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True)
    internal_id = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    url = Column(String, nullable=False)
    captured_date = Column(TIMESTAMP, server_default=func.current_timestamp())

    __table_args__ = (
        Index('properties_internal_provider', 'internal_id', 'provider'),
    )

# Create a sessionmaker factory
Session = sessionmaker(bind=engine)

# Create a new session
session = Session()

# Create the properties table
Base.metadata.create_all(engine)

# You can add further operations using the session object, e.g., adding new entries, querying, etc.
