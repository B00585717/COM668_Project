from decouple import config
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from DBConfig import DBConfig

# Create the engine
engine = create_engine(DBConfig().get_conn_string())

# Create a base class for the model
Base = declarative_base()

# Create the tables if they don't exist
Base.metadata.create_all(engine)


class Voter(Base):
    __tablename__ = 'Voter'

    voter_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    gov_id = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    constituency_id = Column(Integer, ForeignKey('Constituency.constituency_id'), nullable=False)
    email = Column(String, unique=True, nullable=False)


class Constituency(Base):
    __tablename__ = 'Constituency'

    constituency_id = Column(Integer, primary_key=True)
    constituency_name = Column(String)


class Verification(Base):
    __tablename__ = 'Verification'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    otp = Column(String, unique=True, nullable=False)
