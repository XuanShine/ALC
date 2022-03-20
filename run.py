from pywebio import start_server
from pywebio.input import input
from pywebio.output import *
from pywebio_battery import put_logbox

from account import checkConnection

class App:
    def __init__(self):
        self.id = "1"
    
    def login(self, *args):
        put_text(self.id)
        id_ = input("ID:")
        password = input("Mot de Passe:")
        assert checkConnection(id_, password)
        self.id = id_
        put_text(self.id)
        self.menu()
    
    def menu(self):
        put_button
        
    def start(self):
        put_buttons(["Se Connecter", "S’inscrire"], onclick=self.login)

def main():
    App().start()
    
    
start_server(main, port=8080, debug=True)