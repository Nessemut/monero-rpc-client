from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from classes.Output import Output


class OutputService:
    # TODO: FIND A WAY TO MERGE ALL FIELDS OF KNOWN OUTPUTS

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
            except IntegrityError:
                s.rollback()

        s.close()

    def update_known_outputs(self, outputs):
        session = sessionmaker()
        session.configure(bind=self.engine)
        s = session()

        for output in outputs:
            try:
                s.add(output)
                s.commit()
            except IntegrityError:
                s.rollback()

        s.close()
