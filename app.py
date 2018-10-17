#-*- encoding: utf-8 -*-

import os
from flask import Flask, session, request, json, g
from flask import url_for
from flask import render_template
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
		
		db = get_table('messages')
		messages = []
		if db.count({}) != 0:
			messages = [i for i in db.find()]
			print(messages[0])
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

		return render_template('footopia.html', messages=messages)

	@app.route('/postmethod', methods=['POST'])
	def get_js_geolocation():
		session['geolocation'] = json.loads(request.data.decode())
		return redirect(url_for('/footopia'))

	import auth
	app.register_blueprint(auth.bp)

	init_app(app)

	return app

if __name__ == '__main__':
	create_app().run(host='0.0.0.0', port=9000, debug=True)