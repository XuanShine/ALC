from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.db.models import Q

from .models import *

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


def search_family(request, family):
    families = data.objects.filter(Q(nom__contains=word))
    return families

def nouveau_PEC(request):
    chambres_disponibles = Chambre.objects.filter(PEC=None).filter(disponible=True)
    return render(request, "gui/newPEC.html", 
                  {chambres_disponibles: chambres_disponibles})
