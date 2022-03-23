import sys

from models import *


def init_fake_datas():
    db.init("local.db")
    with db:
        db.drop_tables([Famille, Membre, Hotel, PEC, Chambre])
        db.create_tables([Famille, Membre, Hotel, PEC, Chambre])
        nguyen = Famille.create(nom="Nguyen")
        paul = Membre.create(prenom="Paul", sexe="M", naissance=date(1994, 10, 25), titre="Père", famille=nguyen, estResponsable=True)
        julie = Membre.create(prenom="Julie", sexe="F", naissance=date(2019, 1, 5), titre="enfant", famille=nguyen)
        nguyen2 = Famille.create(nom="Nguyen")
        jean = Membre.create(prenom="Jean", sexe="M", naissance=date(1995, 12, 1), titre="Père", famille=nguyen2, estResponsable=True)
        sarah = Membre.create(prenom="Sarah", sexe="F", naissance=date(2018, 2, 19), titre="enfant", famille=nguyen2)
        

if __name__ == "__main__":
    if len(sys.argv) == 1:
        init_fake_datas()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "PROD":
            db.init("alc.db")
        elif sys.argv[1] == "TEST":
            db.init(":memory:")