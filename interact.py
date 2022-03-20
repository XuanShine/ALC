from peewee import SqliteDatabase
from playhouse.reflection import generate_models, print_model, print_table_sql

db = SqliteDatabase('alc.db')