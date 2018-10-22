#-*- encoding:utf-8 -*-

import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from bson.objectid import ObjectId

import db as database


bp = Blueprint('auth', __name__)  # , url_prefix='/auth'

@bp.route('/login', methods=('GET', 'POST'))
def login():
	print('test')
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = database.get_table()
		error = None
		user = db.find_one({'username': username})

		if user is None:
			error = 'Incorrect username.'
		elif not user['password'] == password:
			# elif not check_password_hash(user['password'], password):
			error = 'Incorrect password.'

		if error is None:
			session.clear()
			print(type(user['_id']))
			session['user_id'] = str(user['_id'])
			return redirect(url_for('footopia'))

		flash(error)

	return render_template('auth/login.html')

@bp.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = database.get_table()
		error = None

		if not username:
			error = 'Username is required.'
		elif not password:
			error = 'Password is required.'
		elif db.find_one({'username': username}) is not None:
			error = 'User {} is already registered.'.format(username)

		if error is None:
			db.insert_one({"username": username, "password": password})
			return redirect(url_for('auth.login'))

		flash(error)

	return render_template('auth/register.html')

@bp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None
	else:
		g.user = database.get_table().find_one({'_id': ObjectId(user_id)})['username']
		
@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))

def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))

		return view(**kwargs)

	return wrapped_view
