#-*- encoding: utf-8 -*-

from pymongo import MongoClient
from flask import current_app, g

client = MongoClient('mongodb://localhost:27017/')

def get_db():

	if 'db' not in g:
		g.db = client.logindata

	return g.db

def close_db(e=None):
	db = g.pop('db', None)

	if db is not None:
	 	client.close();

def init_app(app):
	app.teardown_appcontext(close_db)

def get_table(table='posts'):
	if not hasattr(g, 'db'):
		g.db = get_db()
	return g.db[table]