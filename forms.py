from flask_wtf import Form
from wtforms import StringField, TextAreaField, DateField, IntegerField
from wtforms.validators import (DataRequired)

from models import Entry

import datetime

class JournalEntryForm(Form):
	title =  StringField("Title", validators=[DataRequired()])
	date =  DateField("Date (DD/MM/YYYY)", format='%d/%m/%Y', validators=[DataRequired()])
	timespent = IntegerField("Time Spent (in min)")
	content = TextAreaField("What I Learned", validators=[DataRequired()])
	resources = TextAreaField("Resources to Remember")