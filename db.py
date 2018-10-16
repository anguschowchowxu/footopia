#-*- encoding: utf-8 -*-

from pymongo import MongoClient
from flask import current_app, g


def get_db():

	if 'db' not in g:
		client = MongoClient('mongodb://localhost:27017/')
		g.db = client.logindata.posts
		posts = g.db.posts

	return g.db

def close_db(e=None):
	db = g.pop('db', None)

	# if db is not None:
	# 	db.close();

def init_db():
	db = get_db()