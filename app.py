#-*- encoding: utf-8 -*-

import os
from flask import Flask, session, request, json, g, redirect
from flask import url_for
from flask import render_template
from bson.objectid import ObjectId

from db import init_app, get_table

from datetime import datetime


def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
	)

	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# load the test config if passed in
		app.config.from_mapping(test_config)

	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	# a simple page that says hello
	@app.route('/hello')
	def hello():
		return 'Hello, World!'

	@app.route('/')
	def index():
		return render_template('index.html')

	@app.route('/footopia',methods=['GET','POST'])
	def footopia():
		if not g.user:
			return redirect(url_for('auth.login'))
		
		def toString(d):
			for i in d.keys():
				if type(d[i]) == bytes:
					d[i] = d[i].decode('utf-8').replace('\n','').replace('\r','')
			return d

		db = get_table('messages')

		if request.method == 'POST':
			data = request.values
			if g.user:
				username =  g.user
			else:
				username = 'anonymous'
			message = data['message'].encode('utf-8')
			geo = session['geolocation']
			db.insert_one({'username': username, 'lat': geo['lat'], 
							'lng': geo['lng'], 'message': message, 
							'timestamp': datetime.utcnow().strftime('%y-%m-%d %H:%M')})

		messages = []
		if db.count({}) != 0:
			messages = [toString(i) for i in db.find()]
			print(messages[-1])

		return render_template('footopia.html', messages=messages[::-1], username=g.user)

	@app.route('/postmethod', methods=['POST'])
	def get_js_geolocation():
		session['geolocation'] = json.loads(request.data.decode())
		return redirect(url_for('footopia'))

	import auth
	app.register_blueprint(auth.bp)

	init_app(app)

	return app

if __name__ == '__main__':
	create_app().run(host='0.0.0.0', port=9000, debug=True)