from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from model import Ring, Output


class Dao:

    def __init__(self, engine):
        self.engine = engine

    def get_output(self, key):
        session = sessionmaker()
        session.configure(bind=self.engine)
        s = session()
        out = s.query(Output).get(key)
        s.close()
        return out

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

    def get_ring(self, ki):
        session = sessionmaker()
        session.configure(bind=self.engine)
        s = session()
        ring = s.query(Ring).get(ki)
        s.close()
        return ring

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

    def get_known_outputs(self):
        session = sessionmaker()
        session.configure(bind=self.engine)
        s = session()
        outs = s.query(Output).order_by(Output.key).filter(Output.key_image.isnot(None))
        s.close()
        return outs

    def get_rings(self, first_block):
        # NOTE: this takes an insane amount of time to complete
        session = sessionmaker()
        session.configure(bind=self.engine)
        s = session()
        rings = s.query(Ring).filter(Ring.height > first_block).all()
        s.close()
        return rings

    def get_rings_in_tx(self, tx):
        session = sessionmaker()
        session.configure(bind=self.engine)
        s = session()
        rings = s.query(Ring).filter(Ring.transaction == tx).all()
        s.close()
        return rings

    def get_own_spent_outputs(self):
        session = sessionmaker()
        session.configure(bind=self.engine)
        s = session()
        key_images = s.query(Output).filter(Output.key_image.isnot(None), Output.spent).all()
        s.close()
        return key_images

    def mark_output_in_ring(self, output, key_image, mark_as, mark_if_mine):
        operator = '' if mark_if_mine else '!'
        pubkey = '"' + output.key + '"'
        key_image = '"' + key_image + '"'
        con = self.engine.connect()
        query = text("""
            update association_table set `real`= """ + str(mark_as) + """ 
            where output_pubkey = """ + pubkey + """
            and ring_ki""" + operator + """= """ + key_image + """;
        """)
        con.execute(query)

    def last_persisted_ring(self):
        session = sessionmaker()
        session.configure(bind=self.engine)
        s = session()
        last = int(s.query(func.max(Ring.height)).one()[0])
        s.close()
        return last

    def other_rings_with_at_least_one_own_decoy(self):
        con = self.engine.connect()
        query = text("""
            select key_image from ring 
            where ring.key_image not in (select key_image from output where output.key_image is not null)
            and ring.key_image in (select ring_ki from association_table where `real` = 0);
        """)
        key_images = con.execute(query).fetchall()
        return key_images

    def get_remaining_outputs_from_ring_with_decoys(self, key_image):
        key_image = '"' + key_image + '"'
        con = self.engine.connect()
        query = text("""select count(*) from association_table where ring_ki = """ + key_image + """;""")
        total = con.execute(query).fetchone()[0]
        query = text("""select count(`real`) from association_table where ring_ki = """ + key_image + """;""")
        decoys = con.execute(query).fetchone()[0]
        return total - decoys - 1
