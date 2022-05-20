from pywebio.output import *
from pywebio.input import *
from pywebio.pin import *
from pywebio.session import local

from functools import partial
from datetime import datetime

def sure(ifYes, ifNo, text="Êtes-vous sûr ?", textOui="Oui", textNon="Non"):
    def wrapper(f):
        close_popup()
        return f()
    with popup(text, implicit_close=True) as s:
        put_row([
            put_button(textOui, onclick=partial(wrapper, ifYes)),
            put_button(textNon, onclick=partial(wrapper, ifNo))
        ])


def selectCalendar(func, funcReturn, famille):
    date = input("Date :", type="date")
    func(datetime.strptime(date, "%Y-%m-%d").date())
    return funcReturn(famille.id)