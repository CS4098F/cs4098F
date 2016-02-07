from flask.ext.wtf import Form
from wtforms.fields import TextField, TextAreaField, SubmitField
import wtforms

class ItemForm(Form):

    submit = SubmitField('Submit')