from pywebio import start_server
from pywebio.input import input
from pywebio.output import *
from pywebio_battery import put_logbox
from pywebio.pin import *


class Famille:
    @staticmethod
    def ajoutFamille(*args):
        def putNewLine(n, nameFamily=""):
            put_row([ 
                put_input(f"nom{n}", value=nameFamily),
                put_input(f"prenom{n}"),
                put_select(f"sexe{n}",
                           options=[("Autre", "A"),
                                   ("Masculin", "M"),
                                   ("Feminin", "F")]),
                put_input(f"naissance{n}", type="date"),
                put_input(f"titre{n}"),
                put_checkbox(f"responsable{n}", options=["oui"]),
                put_buttons("-")
            ])
        

        put_input("nomFamille", label="Nom de Famille")
        put_input("telephone", label="Telephone")
        put_input("notes", label="Notes")
        entete = ["Nom", "Prénom", "sexe", "Naissance dd/MM/YYYY", "Titre (père, mère, enfant)", "Est Responsable", "Action"]
        put_row(list(map(lambda x: put_text(x), entete)))
        
        # preInputs = ["nom", "prenom", "sexe", "naissance", "titre", "estResponsable"]
        put_buttons(["Add"], onclick=lambda _: putNewLine(1, pin["nomFamille"]))
            
            
        
        