import os
import datetime

from mongoengine import *

connect('apps', username=os.environ['APPS_USER'], password=os.environ['APPS_PASS'])

class LiveBlogUpdate(EmbeddedDocument):
	content = StringField()
	headline = StringField()
	author = StringField()
	timestamp = DateTimeField()

class LiveBlog(Document):
	name = StringField()
	slug = StringField()
	description = StringField()
	updates = ListField(EmbeddedDocumentField(LiveBlogUpdate))
	active = BooleanField(default=False)
	created = DateTimeField()
	modified = DateTimeField()

	@property
	def updates_sorted(self):
		return sorted(self.updates, key=lambda update:update['timestamp'], reverse=True)

	@property
	def updates_count(self):
		return 0

	@property
	def active_label(self):
		if self.active == True:
			return 'true'

		return 'false'