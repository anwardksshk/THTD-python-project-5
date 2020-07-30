from peewee import *

import datetime
import sys

DATABASE = SqliteDatabase('journal.db')

class Entry(Model):
	entry_id = IntegerField(primary_key=True, unique=True)
	title = CharField(max_length=255, default="Untitled")
	timestamp = DateTimeField(default=datetime.datetime.now)
	timespent = IntegerField()
	content = TextField()
	resources = TextField()
	

	class Meta:
		database = DATABASE
		order_by = ('-timestamp')


	@classmethod
	def create_entry(cls, title, content):
		cls.create(title=title, content=content)


class initialize():
	DATABASE.connect()
	DATABASE.create_tables([Entry], safe=True)
	DATABASE.close()