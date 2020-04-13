from datetime import datetime

from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

import forms

##----------------------------------------SETUP----------------------------------------##

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chores.db'
app.config['SECRET_KEY'] = "doodles"
db = SQLAlchemy(app)

##----------------------------------------MODELS----------------------------------------##
## These are essentially DB schemas
class Chores(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    chore = db.Column(db.String(100), nullable=False)
    user = db.Column(db.String, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return 'Chore ' + str(self.id)

##----------------------------------------ROUTES----------------------------------------##
@app.route('/')
def index():
    return render_template('home.html')

## New Chore
@app.route('/new_chore', methods=['GET', 'POST'])
def new_chore():
    form = forms.NewChoreForm()
    if form.validate_on_submit():
        db.session.add(Chores(user=form.username.data, chore=form.chore.data))
        db.session.commit()
        ## Empty the fields
        form = forms.NewChoreForm(formdata=None)
    return render_template('new_chores.html', form=form)

## Delete Chore
@app.route('/delete_chore', methods=['GET', 'POST'])
def delete_chore():
    form = forms.DeleteChoreForm()
    if form.validate_on_submit():
        Chores.query.filter_by(id=form.id.data).delete()
        db.session.commit()
        ## Empty the fields
        form = forms.DeleteChoreForm(formdata=None)
    return render_template('delete_chore.html', form=form)

## Chore Table
@app.route('/chore_board', methods=['GET', 'POST'])
def display_chore_board():
    ## sqlite doesn't do disticnt on() so we need to work around it a little
    chores = db.engine.execute(
        """SELECT id, user, chore, MAX(datetime(datetime)) AS datetime, ((STRFTIME('%s','NOW') + 10 * 3600) - STRFTIME('%s',"datetime")) / 3600 AS diff
        FROM chores
        GROUP BY chore
        ORDER BY datetime DESC"""
        )
    return render_template('chore_board.html', table=chores, data=chores)

## DB init
@app.route('/db_init')
def initiate_database():
    db.create_all()
    return render_template('chore_board.html')

## DB Delete
@app.route('/db_delete', methods = ['GET', 'POST'])
def delete_database():
    form = forms.ResetDatabaseConfirm()
    if form.validate_on_submit():
        db.drop_all()
        db.create_all()
        db.session.commit()
    return render_template('reset_database.html', form=form)

##----------------------------------------MAIN----------------------------------------##

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', threaded=True)

## TODO:
# Actual log-in feature
# change column hours ago to be days when > 24 hours
# Make requirements file