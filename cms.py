#!/usr/bin/env python

import datetime
import json
import os

from bson.objectid import ObjectId
from flask import Flask, render_template, request
from mongoengine import connect

from models import LiveBlog, LiveBlogUpdate

app = Flask(__name__)

connect('apps', username=os.environ['APPS_USER'], password=os.environ['APPS_PASS'])

@app.route('/live-blog/', methods=['GET', 'POST'])
@app.route('/live-blog/<live_blog_id>/', methods=['GET', 'POST'])
@app.route('/live-blog/<live_blog_id>/<form_type>/', methods=['GET', 'POST'])
def live_blog_list(live_blog_id=None, form_type=None):

	now = datetime.datetime.utcnow()
	if request.method == 'GET':
		if live_blog_id == None:

			context = {
				'blogs': LiveBlog.objects 
			}
			return render_template('blog_list.html', **context)

		else:
			object_id = ObjectId(live_blog_id)
			context = {
				'blog': LiveBlog.objects.get(id=object_id)
			}

			return render_template('blog_detail.html', **context)

				
	if request.method == 'POST':

		if live_blog_id == None:

			data = {}

			for item in dict(request.form).items():
				data[item[0]] = item[1][0]

			if data['active'] == u'true':
				data['active'] = True
			else:
				data['active'] = False

			data['updated'] = now
			data['created'] = now

			live_blog = LiveBlog(**data)
			live_blog.save()

			return LiveBlog.id.__str__()

		else:
			object_id = ObjectId(live_blog_id)
			live_blog = LiveBlog.objects.get(id=object_id)

			if form_type == None:
				# Neither updating the Live Blor nor an Update. Should never occur.
				return ''

			else:

				data = {}
				
				for item in dict(request.form).items():
					data[item[0]] = item[1][0]
				
				if form_type == 'update':
					data['timestamp'] = now

					live_blog.updates.append(LiveBlogUpdate(**data))
					live_blog.save()

					return live_blog.id.__str__()

				if form_type == 'blog':

					pass

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)