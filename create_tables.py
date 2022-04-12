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
        
        

if __name__ == "__main__":
    if len(sys.argv) == 1:
        init_fake_datas()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "PROD":
            db.init("alc.db")
        elif sys.argv[1] == "TEST":
            db.init(":memory:")