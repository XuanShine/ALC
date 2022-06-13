import sys

from models import *

from datetime import datetime, date

from werkzeug.security import generate_password_hash, check_password_hash

TABLES = [Famille, Membre, Hotel, PEC, Chambre, User]

def init_fake_datas():
    db.init("local.db")
    with db:
        db.drop_tables(TABLES)
        db.create_tables(TABLES)
        nguyen = Famille.create(nom="Nguyen")
        paul = Membre.create(prenom="Paul", sexe="M", naissance=date(1994, 10, 25), titre="Père", famille=nguyen, estResponsable=True)
        fils1 = Membre.create(prenom="Edoardo", sexe="M", naissance=date(2019, 1, 5), titre="enfant", famille=nguyen)
        nguyen2 = Famille.create(nom="Nguyen")
        jean = Membre.create(prenom="Jean", sexe="M", naissance=date(1995, 12, 1), titre="Père", famille=nguyen2, estResponsable=True)
        julie = Membre.create(prenom="Julie", sexe="F", naissance=date(2018, 2, 19), titre="enfant", famille=nguyen2)
        
        panorama = Hotel(nom="Panorama",
                         hotelname="hotelpanorama",
                         adresse="2 Cours Honoré Cresp, 06130 Grasse",
                         ville="Grasse",
                         cp = "06130",
                         telephone = "0493368080",
                         mail = "hotelpanorama@wanadoo.fr")
        panorama.save()
        rooms = [200 + i for i in range(1, 9)]
        rooms2 = [300 + i for i in range(1, 9)]
        for room, room2 in zip(rooms, rooms2):
            Chambre.create(numero=str(room),
                           convention=True,
                           capacite=3,
                           disponible=True,
                           prix=50,
                           hotel=panorama)
            Chambre.create(numero=str(room2),
                           convention=False,
                           capacite=3,
                           disponible=False,
                           prix=50,
                           hotel=panorama)
        
        laposte = Hotel(nom="Hotel de la Poste",
                        hotelname="hotellaposte",
                        adresse="106 Chemin Qurnade, 06530 Peymeinade",
                        ville="Peymeinade",
                        cp = "06530",
                        telephone = "0493332136",
                        mail = "hotelposte@gmail.com")
        laposte.save()
        rooms = [102 + i for i in range(3)]
        for room in rooms:
            Chambre.create(numero=str(room),
                           convention=False,
                           capacite=2,
                           disponible=True,
                           prix=30,
                           hotel=laposte)
        
        pec = PEC.create(famille=nguyen,
                   date_debut=datetime(2022, 4, 2).date(),
                   date_fin=datetime(2022, 5, 25).date(),
                   derniere_date_facturee=datetime(2022, 5, 1))
        
        pec.setChambres([1])
        
        paul = User.create(username="paul", password=generate_password_hash("auie"), telephone="0651216491")
        
        

if __name__ == "__main__":
    if len(sys.argv) == 1:
        init_fake_datas()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "PROD":
            db.init("alc.db")
        elif sys.argv[1] == "TEST":
            db.init(":memory:")