import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
    

class Family(models.Model):
    nom = models.CharField(max_length=200)

    def __str__(self):
        return self.nom

    def nombre(self):
        return len(self.membre.all())

class Member(models.Model):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    naissance = models.DateField()
    titre = models.CharField(max_length=200)  # père, mère, enfant
    famille = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="membre")

    def __str__(self):
        return self.nom + " " + self.prenom
    
    def age(self):
        return int((timezone.now().date() - self.naissance).days / 365.25)

