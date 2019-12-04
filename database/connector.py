from os import environ
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta
import json
from flask_session import Session

class Manager:
    Base = declarative_base()
    session = None

    def createEngine(self):
        #engine = create_engine('sqlite:///data.db?check_same_thread=False', echo=False)
        engine = create_engine('postgres+psycopg2://xcguopzqvrwaot:c43c68edb95345039c908ab19cbc3a356adccd13bb6f5c4617608fe7f5a86705@ec2-174-129-254-217.compute-1.amazonaws.com:5432/d377csr23ei16d')
        self.Base.metadata.create_all(engine)
        return engine

    def getSession(self, engine):
        if self.session == None:
            Session = sessionmaker(bind=engine)
            session = Session()

        return session

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None

            return fields

        return json.JSONEncoder.default(self, obj)
