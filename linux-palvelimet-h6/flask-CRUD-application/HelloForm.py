from flask import Flask, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.secret_key = "aez2Caipootohd2ahph1zie5aefoh0"
db = SQLAlchemy(app)

class Text(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String, nullable=False)
	name = db.Column(db.String, nullable=False)

TextForm = model_form(Text, base_class=FlaskForm, db_session=db.session)

@app.before_first_request
def initMe():
	db.create_all()

	text = Text(text="Morjens!", name="Pulkkinen")
	db.session.add(text)

	text = Text(text="terve", name="Dille")
	db.session.add(text)
	db.session.commit()

@app.route("/")
def index():
	texts = Text.query.all()
	return render_template("index.html", texts=texts)

@app.route("/<int:id>/delete")
def deleteText(id):
	text = Text.query.get_or_404(id)
	db.session.delete(text)
	db.session.commit()

	flash("Text deleted")
	return redirect("/")

@app.route("/<int:id>/edit", methods=["GET", "POST"])
@app.route("/form-page", methods=["GET", "POST"])
def addForm(id=None):
	text = Text()
	if id:
		text = Text.query.get_or_404(id)
	
		

	form = TextForm(obj=text)

	if form.validate_on_submit():
		
		form.populate_obj(text)
		
		db.session.add(text)
		db.session.commit()

		print("added text")
		flash("Added")
		return redirect("/")		

	return render_template("form-page.html", form=form)

if __name__ == "__main__":
	app.run()
