from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio_battery import put_logbox
from pywebio.session import local, hold
from pywebio.session import set_env
from pywebio.platform.flask import webio_view
import pywebio
import emojis

from flask import Flask
from requests import request
from werkzeug.security import generate_password_hash, check_password_hash
from functools import partial

from models import *
from account import needLogin


@use_scope("main", clear=True)
@needLogin(role="assistant")
def view(*args, **kwargs):
    put_markdown(r"## Veuillez signaler des bugs ou améliorations possibles.")
    query = Review.select()
    user = User.select().where(User.username == kwargs["username"]).get()
    if len(query) == 0:
        put_text("Aucune requête")
    else:
        put_table(header=["Fini ?", "Requête", "intérêt", "Discussion", "Action"], tdata=[[
            put_text(emojis.encode(":white_check_mark:") if requete.fini else emojis.encode(":x:")),
            put_text(requete.request),
            put_text(f"{requete.popularity} 👍"),
            put_collapse(title="", content=[
                put_scrollable(content=[requete.notes], keep_bottom=True)
            ]),
            put_buttons(buttons=[
                {"label": "Discuter", "value": "discuss"},
                {"label": "👍" if not requete.userDidLike(user) else "👎", "value": "like"}],
                onclick=[partial(discuss, requete, user), partial(requete.like, user, view)])
            
            ] for requete in query
        ])
    action = actions(buttons=[("Ajouter une requete", "add")])
    if action == "add":
        addRequete(user)
    return view()

def discuss(requete, user):
    text = input("Votre message")
    requete.notes = f"{user.username}\n{text}"
    return view()

def addRequete(user):
    text = textarea(placeholder="Votre demande", required=True)
    Review.create(demande=user, request=text)
    return view()