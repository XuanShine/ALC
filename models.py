from peewee import *

db = SqliteDatabase('alc.db')

class BaseModel(Model):
    class Meta:
        database = db


class Famille(BaseModel):
    nom = CharField(max_length=20)

    def responsable(self):
        query = self.membres.filter(est_responsable=True)
        if not query:
            return "Aucun indiqué"
        else:
            return " | ".join(map(str, query))

    def __str__(self):
        return self.nom + " - " + str(self.id)

    def nombre(self):
        return len(self.membres.all())