from wtforms import StringField, SubmitField, IntegerField, validators
from flask_wtf import FlaskForm

## Forms
class NewChoreForm(FlaskForm):
    username = StringField('User', [validators.Length(min=3, max=25), validators.DataRequired()])
    chore = StringField('Chore', [validators.DataRequired()])
    submit = SubmitField('Submit')

class DeleteChoreForm(FlaskForm):
    username = StringField('User', [validators.Length(min=3, max=25), validators.DataRequired()])
    id = IntegerField('Chore ID', [validators.DataRequired()])
    submit = SubmitField('Submit')
