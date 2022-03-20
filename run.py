from turtle import onclick
from pywebio import start_server
from pywebio.input import input
from pywebio.output import *
from pywebio_battery import put_logbox
from famille import Famille

from account import checkConnection

class App:
    def __init__(self):
        self.id = None
    
    def login(self, *args):
        id_ = input("ID:")
        password = input("Mot de Passe:")
        assert checkConnection(id_, password)
        self.id = id_
        put_text(f"ID: {self.id}")
        self.menu()
    
    def menu(self):
        put_buttons(["Ajouter une famille"], onclick=Famille.ajoutFamille)
        
    def start(self):
        # put_buttons(["Se Connecter", "S’inscrire"], onclick=self.login)
        self.menu()

def main():
    App().start()
    
    
start_server(main, port=8080, debug=True)