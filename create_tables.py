import os, sys

C = os.path.abspath(os.path.dirname(__file__))
sys.path.append(C)

from models import *

import csv
from random import choice, randint, shuffle

from datetime import datetime, date

from werkzeug.security import generate_password_hash, check_password_hash

TABLES = [Famille, Membre, Hotel, PEC, Chambre, User]

def init_fake_datas():
    db.init(sys.path.join(C, "local.db"))
    with db:
        db.drop_tables(TABLES)
        db.create_tables(TABLES)
        nguyen = Famille.create(nom="Nguyen")
        paul = Membre.create(prenom="Paul", sexe="M", naissance=date(1994, 10, 25), titre="Père", famille=nguyen, estResponsable=True)
        fils1 = Membre.create(prenom="Edoardo", sexe="M", naissance=date(2019, 1, 5), titre="enfant", famille=nguyen)
        nguyen2 = Famille.create(nom="Nguyen")
        jean = Membre.create(prenom="Jean", sexe="M", naissance=date(1995, 12, 1), titre="Père", famille=nguyen2, estResponsable=True)
        julie = Membre.create(prenom="Julie", sexe="F", naissance=date(2018, 2, 19), titre="enfant", famille=nguyen2)
        
        aroma = User.create(username="aroma", telephone="0651216491", password=generate_password_hash("bépo"), role="hotel")
        hocine = User.create(username="hocine", telephone="0651216491", password=generate_password_hash("bépo"), role="hotel")
        panorama = Hotel(nom="Panorama",
                         hotelname="hotelpanorama",
                         owner=aroma,
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
                           disponible=bool(choice([0, 1])),
                           prix=50,
                           hotel=panorama)
        
        laposte = Hotel(nom="Hotel de la Poste",
                        hotelname="hotellaposte",
                        owner=hocine,
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
        
        # pec = PEC.create(famille=nguyen,
        #            date_debut=datetime(2022, 4, 2).date(),
        #            date_fin=datetime(2022, 5, 25).date(),
        #            derniere_date_facturee=datetime(2022, 5, 1))
        
        # pec.setChambres([1])
        
        paul = User.create(username="Geraldine", password=generate_password_hash("auie"), telephone="0651216491", role="assistant")
        jean = User.create(username="jean", password=generate_password_hash("auie"), telephone="0651216491", role="directeur")
        
        nefliu = Famille.create(nom="Nefliu")
        veronica = Membre.create(prenom="Veronica Adriana", sexe="F", naissance=date(1983, 7, 4), titre="Mère", famille=nefliu, estResponsable=True)
        fille = Membre.create(prenom="Sarah", nom="Petre", sexe="F", naissance=date(2017, 8, 18), titre="enfant", famille=nefliu)
        pec = PEC.create(famille=nefliu,
                   date_debut=datetime(2022, 5, 4).date(),
                   date_fin=datetime(2022, 7, 8).date(),
                   derniere_date_facturee=datetime(2022, 6, 1))
        ch201 = Chambre.select().join(Hotel).where((Chambre.numero == "201") & (Hotel.nom == "Panorama")).get()
        pec.setChambres([ch201])
        
        sabekia = Famille.create(nom="Sabekia")
        mère = Membre.create(prenom="Aza", sexe="F", naissance=date(1977, 8, 11), titre="mère", famille=sabekia)
        fils1 = Membre.create(prenom="Vakhtang", sexe="M", naissance=date(2005, 1, 18), titre="enfant", famille=sabekia)
        fille1 = Membre.create(prenom="Ana", sexe="F", naissance=date(2006, 8, 18), titre="enfant", famille=sabekia)
        fille2 = Membre.create(prenom="Marie", nom="Gigineshvili", sexe="F", naissance=date(2021, 5, 27), titre="enfant", famille=sabekia)
        pec = PEC.create(famille=sabekia,
                   date_debut=datetime(2022, 3, 4).date(),
                   date_fin=datetime(2022, 7, 4).date(),
                   derniere_date_facturee=datetime(2022, 6, 1))
        ch202 = Chambre.select().join(Hotel).where((Chambre.numero == "202") & (Hotel.nom == "Panorama")).get()
        pec.setChambres([ch202])
        
        fekih = Famille.create(nom="FEKIH")
        mère = Membre.create(prenom="Manel", sexe="F", naissance=date(1985, 10, 12), titre="mère", famille=fekih)
        fils1 = Membre.create(prenom="Iskander", nom="Boumiza", sexe="M", naissance=date(2009, 11, 3), titre="enfant", famille=fekih)
        fils2 = Membre.create(prenom="Chahd", nom="Boumiza", sexe="M", naissance=date(2012, 4, 1), titre="enfant", famille=fekih)
        pec = PEC.create(famille=fekih,
                   date_debut=datetime(2022, 5, 31).date(),
                   date_fin=datetime(2022, 7, 14).date(),
                   derniere_date_facturee=datetime(2022, 6, 1))
        ch203 = Chambre.select().join(Hotel).where((Chambre.numero == "203") & (Hotel.nom == "Panorama")).get()
        pec.setChambres([ch203])
        
        bourouba = Famille.create(nom="Bourouba")
        père = Membre.create(prenom="Abd Hac", sexe="M", naissance=date(1963, 4, 6), titre="père", famille=bourouba)
        fils1 = Membre.create(prenom="Houssem", sexe="M", naissance=date(2000, 2, 17), titre="enfant", famille=bourouba)
        fils2 = Membre.create(prenom="Ahmed", sexe="M", naissance=date(2002, 8, 9), titre="enfant", famille=bourouba)
        pec = PEC.create(famille=bourouba,
                   date_debut=datetime(2022, 5, 31).date(),
                   date_fin=datetime(2022, 7, 8).date(),
                   derniere_date_facturee=datetime(2022, 6, 1))
        ch204 = Chambre.select().join(Hotel).where((Chambre.numero == "204") & (Hotel.nom == "Panorama")).get()
        pec.setChambres([ch204])
        
        gubkina = Famille.create(nom="Gubkina")
        femme = Membre.create(prenom="Marina", sexe="F", naissance=date(1980, 3, 24), titre="femme seule", famille=gubkina)
        pec = PEC.create(famille=gubkina,
                   date_debut=datetime(2022, 4, 26).date(),
                   date_fin=datetime(2022, 6, 17).date(),
                   derniere_date_facturee=datetime(2022, 6, 1))
        ch205 = Chambre.select().join(Hotel).where((Chambre.numero == "205") & (Hotel.nom == "Panorama")).get()
        pec.setChambres([ch205])
        
        njintaa = Famille.create(nom="Njintaa")
        mère = Membre.create(prenom="Andrelyn", sexe="F", naissance=date(1981, 2, 28), titre="mère", famille=njintaa, estResponsable=True)
        fils1 = Membre.create(prenom="Sakira", sexe="F", naissance=date(2015, 1, 2), titre="enfant", famille=njintaa)
        fils2 = Membre.create(prenom="Nabil", sexe="M", naissance=date(2016, 8, 16), titre="enfant", famille=njintaa)
        pec = PEC.create(famille=njintaa,
                   date_debut=datetime(2022, 5, 24).date(),
                   date_fin=datetime(2022, 6, 24).date(),
                   derniere_date_facturee=datetime(2022, 6, 1))
        ch206 = Chambre.select().join(Hotel).where((Chambre.numero == "206") & (Hotel.nom == "Panorama")).get()
        pec.setChambres([ch206])
        
        klai = Famille.create(nom="Klai")
        veronica = Membre.create(prenom="Henda", sexe="F", naissance=date(1994, 7, 11), titre="Mère", famille=klai, estResponsable=True)
        fille = Membre.create(prenom="Haroun", sexe="M", naissance=date(2018, 7, 20), titre="enfant", famille=klai)
        pec = PEC.create(famille=klai,
                   date_debut=datetime(2021, 10, 14).date(),
                   date_fin=datetime(2022, 7, 17).date(),
                   derniere_date_facturee=datetime(2022, 6, 1))
        ch207 = Chambre.select().join(Hotel).where((Chambre.numero == "207") & (Hotel.nom == "Panorama")).get()
        pec.setChambres([ch207])
        
        hamila = Famille.create(nom="hamila")
        femme = Membre.create(prenom="Rihab", sexe="F", naissance=date(1993, 3, 31), titre="mère", famille=hamila, estResponsable=True)
        père = Membre.create(prenom="Anis", sexe="M", naissance=date(1986, 11, 15), titre="père", famille=hamila, estResponsable=True)
        fille = Membre.create(prenom="Hyhana", sexe="M", naissance=date(2020, 9, 11), titre="enfant", famille=hamila)
        pec = PEC.create(famille=hamila,
                   date_debut=datetime(2022, 4, 15).date(),
                   date_fin=datetime(2022, 5, 15).date(),
                   derniere_date_facturee=datetime(2022, 6, 1))
        ch208 = Chambre.select().join(Hotel).where((Chambre.numero == "208") & (Hotel.nom == "Panorama")).get()
        pec.setChambres([ch208])
        
        with open(sys.path.join(C, "mock_cp.txt"), "r", encoding="utf8") as f_in:
            data = f_in.readlines()
        cp = dict()
        for line in data:
            city, code = line.split("06")
            cp[f"06{code}"] = city
        
        hotels = []
        with open(sys.path.join(C, "mock_hotel.csv"), "r", encoding="utf8") as f_in:
            reader = csv.reader(f_in)
            reader.__next__()
            for row in reader:
                code_postal = choice(list(cp.keys()))
                ville = cp[code_postal]
                hotel = Hotel.create(nom=row[0],
                                hotelname=row[0].casefold(),
                                adresse=f"{row[1]}, {code_postal} {ville}",
                                ville=ville,
                                cp = code_postal,
                                telephone = row[2],
                                mail = row[3])
                hotels.append(hotel)
                
                # Chambres
                centaine = randint(1, 6)
                nombre = randint(3, 9)
                for i in range(nombre):
                    i += 1
                    Chambre.create(numero=f"{centaine}0{i}",
                           convention=bool(choice([0, 1])),
                           capacite=randint(1, 3),
                           disponible=bool(choice([0, 1])),
                           prix=randint(3, 5) * 10 + randint(0, 1) * 5,
                           hotel=hotel)
        
        # Famille
        nom = set()
        prenom = set()
        with open(sys.path.join(C, "mock_name.csv"), "r", encoding="utf8") as f_in:
            reader = csv.reader(f_in)
            reader.__next__()
            for row in reader:
                nom.add(row[1])
                prenom.add(row[0])
        familles = []
        for i in range(20):
            famille = Famille.create(nom=choice(list(nom)))
            for j in range(randint(1, 5)):
                if j == 0:
                    mère = Membre.create(prenom=choice(list(prenom)), sexe=choice(["F", "M"]), naissance=date(randint(1970, 1994), randint(1, 12), randint(1, 28)), titre="parent", famille=famille, estResponsable=True)
                else:
                    enfant = Membre.create(prenom=choice(list(prenom)), sexe=choice(["F", "M"]), naissance=date(randint(2000, 2021), randint(1, 12), randint(1, 28)), titre="enfant", famille=famille, estResponsable=True)
            familles.append(famille)
        
        # PEC
        for famille in familles:
            pec = PEC.create(famille=famille,
                    date_debut=datetime(2022, randint(1, 5), randint(1, 28)).date(),
                    date_fin=datetime(2022, randint(6, 7), randint(1, 28)).date(),
                    derniere_date_facturee=datetime(2022, 6, 1))
            query = Chambre.select()
            a = list(query)
            shuffle(a)
            for chambre in a:
                if not chambre.disponible:
                    continue
                else:
                    pec.setChambres([chambre])
                    break

                

if __name__ == "__main__":
    if len(sys.argv) == 1:
        init_fake_datas()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "PROD":
            db.init("alc.db")
        elif sys.argv[1] == "TEST":
            db.init(":memory:")