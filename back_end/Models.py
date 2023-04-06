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

    votes = relationship("Votes", back_populates="voter")

    def get_password(self):
        return self.password


class Constituency(Base):
    __tablename__ = 'Constituency'

    constituency_id = Column(Integer, primary_key=True)
    constituency_name = Column(String)


class Verification(Base):
    __tablename__ = 'Verification'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    otp = Column(String, unique=True, nullable=False)

class Party(Base):
    __tablename__ = 'Party'

    party_id = Column(Integer, primary_key=True)
    party_name = Column(String, unique=True, nullable=False)
    image = Column(String, unique=False, nullable=False)
    manifesto = Column(String, unique=False, nullable=False)


class Candidate(Base):
    __tablename__ = 'Candidate'

    candidate_id = Column(Integer, primary_key=True)
    candidate_firstname = Column(String, unique=False, nullable=False)
    candidate_lastname = Column(String, unique=False, nullable=False)
    party_id = Column(Integer, unique=False, nullable=False)
    vote_count = Column(Integer, unique=False, nullable=True)
    image = Column(String, unique=False, nullable=False)
    constituency_id = Column(Integer, unique=False, nullable=True)
    statement = Column(String, unique=False, nullable=False)

    votes = relationship("Votes", back_populates="candidate")


class Votes(Base):
    __tablename__ = 'Votes'

    vote_id = Column(Integer, primary_key=True)
    voter_id = Column(Integer, ForeignKey('Voter.voter_id'), nullable=False)
    candidate_id = Column(Integer, ForeignKey('Candidate.candidate_id'), nullable=False)

    # Relationships
    voter = relationship("Voter", back_populates="votes")
    candidate = relationship("Candidate", back_populates="votes")
