from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio_battery import put_logbox
from pywebio.session import local
from pywebio.session import set_env
from pywebio import session
from pywebio.platform.flask import webio_view
import pywebio

from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
from functools import partial

from models import User

import alerte
from famille import GestionFamille
import hebergement as hotel
from create_tables import init_fake_datas
from account import checkConnection, login, logout, needLogin
import hotelier

app = Flask(__name__)

class App:
    def __init__(self):
        self.id = None
    
    @needLogin(role="all")
    def start(self, **kwargs):
        if session.info.user_agent.is_mobile:
            set_env(input_panel_fixed=False, input_auto_focus=False, output_max_width="100%")
        else:
            set_env(output_max_width="80%")
        pywebio.config(title="ALC", description="Logiciel de gestion PAU")
        # breakpoint()
        if kwargs["role"] == "assistant":
            self.menuUser()
        elif kwargs["role"] == "hotel":
            self.menuHotel()
        # breakpoint()
    
    def logout(self):
        clear("all")
        logout()
        return self.start()

    @needLogin(role="hotel")
    @use_scope("all", clear=True)
    def menuHotel(self, **kwargs):
        put_text(f"Bonjour {kwargs['username']}")
        put_buttons(buttons=[
            "Gérer les hébergements",
            "Déconnexion"
        ], onclick=[
            partial(self.menuHotel, **kwargs),
            self.logout
        ])
        put_scope("main")
        hotelier.connect(**kwargs)
    
    @needLogin(role="assistant")
    @use_scope("all", clear=True)
    def menuUser(self, **kwargs):
        put_text(f"Bonjour {kwargs['username']}")
        put_buttons(buttons=[
            "Ajouter / Rechercher une famille",
            "Gérer les hébergements",
            "Voir les alertes",
            "Déconnexion"
        ], onclick=[
            GestionFamille.formAjoutFamille,
            hotel.gestion,
            alerte.view,
            self.logout
        ])
        put_scope("famille")
        put_scope("main")
        actions(buttons=["Continue"])
        return self.menuUser()


def main():
    App().start()
    
init_fake_datas()


start_server(main, port=5001, debug=True, host="0.0.0.0")

# app.add_url_rule("/", "webio_view", webio_view(App().start, cdn="https://cdn.jsdelivr.net/gh/wang0618/PyWebIO-assets@v1.6.1/"), methods=["GET", "POST", "OPTIONS"])


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=5001)
    # pywebio.platform.flask.start_server(App().start, port=8080, debug=True)
    pass
