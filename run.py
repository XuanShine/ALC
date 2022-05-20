from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio_battery import put_logbox
from pywebio.session import local
from pywebio.session import set_env

from functools import partial

from famille import GestionFamille
import hebergement as hotel
from create_tables import init_fake_datas
from account import checkConnection

class App:
    def __init__(self):
        self.id = None
        
    def start(self):
        set_env(output_max_width="80%")
        # put_buttons(["Se Connecter", "S’inscrire"], onclick=self.login)
        self.menu()
        return
    
    def login(self, *args):
        id_ = input("ID:")
        password = input("Mot de Passe:")
        assert checkConnection(id_, password)
        self.id = id_
        put_text(f"ID: {self.id}")
        self.menu()
        return
    
    def menu(self):
        put_buttons(buttons=[
            "Ajouter / Rechercher une famille",
            "Gérer les hébergements"
        ], onclick=[
            GestionFamille.formAjoutFamille,
            hotel.gestion
        ])
        put_scope("famille")
        put_scope("main")
        return

def main():
    App().start()
    
init_fake_datas()

start_server(main, port=8080, debug=True)