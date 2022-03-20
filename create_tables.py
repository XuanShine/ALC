from models import *

def create_tables():
    with db:
        db.create_tables([Famille, Membre, Hotel, PEC, Chambre])


def init_fake_datas():
    db = SqliteDatabase('test.db')
    
    with 

create_tables()