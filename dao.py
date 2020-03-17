from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from model import Ring, Output


class Dao:

    def __init__(self, engine):
        self.engine = engine

    def save_outputs(self, outputs):
        session = sessionmaker()
        session.configure(bind=self.engine)
        s = session()

        for output in outputs:
            try:
                s.add(output)
                s.commit()
            except (IntegrityError, InvalidRequestError):
                s.rollback()

        s.close()

    def save_ring(self, ring):
        session = sessionmaker()
        session.configure(bind=self.engine)
        s = session()
        try:
            s.add(ring)
            s.commit()
        except (IntegrityError, InvalidRequestError):
            s.rollback()

        s.close()

    def get_ring(self, ki):
        session = sessionmaker()
        session.configure(bind=self.engine)
        s = session()
        ring = s.query(Ring).get(ki)
        s.close()
        return ring

    def get_output(self, key):
        session = sessionmaker()
        session.configure(bind=self.engine)
        s = session()
        out = s.query(Output).get(key)
        s.close()
        return out
