import sys

from models import *


def init_fake_datas():
    db.init("local.db")
    with db:
        db.drop_tables([Famille, Membre, Hotel, PEC, Chambre])
        db.create_tables([Famille, Membre, Hotel, PEC, Chambre])
        Famille.create(nom="Nguyen")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        init_fake_datas()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "PROD":
            db.init("alc.db")
        elif sys.argv[1] == "TEST":
            db.init(":memory:")