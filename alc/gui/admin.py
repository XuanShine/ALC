from django.contrib import admin

# Register your models here.
from .models import *

class MembreInline(admin.TabularInline):
    model = Membre
    extra = 0

class MembreAdmin(admin.ModelAdmin):
    list_display = ("nom", "prenom", "naissance", "famille")


class FamilleAdmin(admin.ModelAdmin):
    fields = ["nom"]
    inlines = [MembreInline]

    list_display = ("nom", "responsable")

admin.site.register(Famille, FamilleAdmin)
admin.site.register(Membre, MembreAdmin)

class ChambreInline(admin.TabularInline):
    model = Chambre
    extra = 1

class HotelAdmin(admin.ModelAdmin):
    inlines = [ChambreInline]

    list_display = ("nom", "adresse", "telephone", "mail", "disponibilite")

admin.site.register(Hotel, HotelAdmin)
admin.site.register(Chambre)

class PECAdmin(admin.ModelAdmin):
    inlines = [ChambreInline]

admin.site.register(PEC, PECAdmin)
