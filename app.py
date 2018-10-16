#-*- encoding: utf-8 -*-

import os
from flask import Flask
from flask import url_for
from flask import render_template
from db import init_db

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

	import auth
	app.register_blueprint(auth.bp)

	# init_db(app)  # ? 

	return app

if __name__ == '__main__':
	create_app().run(host='0.0.0.0', port=9000, debug=True)