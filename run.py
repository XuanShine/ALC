from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio_battery import put_logbox
from pywebio.session import local
from pywebio.session import set_env
from pywebio.platform.flask import webio_view
import pywebio

from flask import Flask
from functools import partial

from famille import GestionFamille
import hebergement as hotel
from create_tables import init_fake_datas
from account import checkConnection

app = Flask(__name__)

class App:
    def __init__(self):
        self.id = None
        
    def start(self):
        set_env(output_max_width="80%")
        # put_buttons(["Se Connecter", "S’inscrire"], onclick=self.login)
        self.menu()

    
    def login(self, *args):
        id_ = input("ID:")
        password = input("Mot de Passe:")
        assert checkConnection(id_, password)
        self.id = id_
        put_text(f"ID: {self.id}")
        self.menu()

    
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


def main():
    App().start()
    
init_fake_datas()


start_server(main, port=5001, debug=True, host="0.0.0.0")

# app.add_url_rule("/", "webio_view", webio_view(App().start, cdn="https://cdn.jsdelivr.net/gh/wang0618/PyWebIO-assets@v1.6.1/"), methods=["GET", "POST", "OPTIONS"])


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=5001)
    # pywebio.platform.flask.start_server(App().start, port=8080, debug=True)
    pass
