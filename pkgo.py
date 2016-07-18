# pkgo
# A simple app to track pokemon caught in Pokemon Go.

import os

from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, IntegerField, DateField
from wtforms.validators import DataRequired

# app init
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'pkgo.db')
db = SQLAlchemy(app)

# model constants
short_text = 20
long_text = 100

# models
class Pokemon(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)

	species = db.Column(db.String(long_text))
	name = db.Column(db.String(long_text))
	primary_type = db.Column(db.String(short_text))
	secondary_type = db.Column(db.String(short_text))
	power = db.Column(db.Integer)

	def __init__(self, species, name, primary_type, secondary_type, power):
		self.species = species
		self.name = name
		self.primary_type = primary_type
		self.secondary_type = secondary_type
		self.power = power

	def __repr__(self):
		return 'Pokemon({}, {}, {}, {}, {})'.format(
			self.species,
			self.name,
			self.primary_type,
			self.secondary_type,
			self.power)

# forms
class PokemonForm(Form):
	species = StringField('Species', validators=[DataRequired()])
	name = StringField('Name', validators=[DataRequired()])
	primary_type = StringField('Type 1', validators=[DataRequired()])
	secondary_type = StringField('Type 2', validators=[DataRequired()])
	power = IntegerField('Combat power', validators=[DataRequired()])

# views
@app.route("/")
def list():
	pokemon = Pokemon.query.all()
	return render_template('list.html',
		title="My Pokemon",
		pokemon=pokemon)

@app.route("/register/", methods=['GET', 'POST'])
def add():
	form = PokemonForm()
	if form.validate_on_submit():
		p = Pokemon(
			form.species.data,
			form.name.data,
			form.primary_type.data,
			form.secondary_type.data,
			form.power.data)
		db.session.add(p)
		db.session.commit()
		return redirect(url_for('list'))
	return render_template('add.html',
		title="Register a Pokemon",
		form=form)

# run app
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)