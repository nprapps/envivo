#!/usr/bin/env python

import datetime
import json
import os

from bson.objectid import ObjectId
from flask import Flask, request
from mongoengine import connect

from models import LiveBlog

app = Flask(__name__)

db = connect('apps', username=os.environ['APPS_USER'], password=os.environ['APPS_PASS'])

@app.route('/live-blog/<live_blog_id>/', methods=['GET', 'POST'])
def live_blog_list(live_blog_id):

	if request.method == 'GET':

		object_id = ObjectId(live_blog_id)
		blog = LiveBlog.objects.get(id=object_id)
		blog_dict = blog._data
		raw_updates = blog_dict['updates']

		blog_dict['updates'] = []
		for update in raw_updates:
			update_dict = update._data
			for item in update_dict.items():
				if isinstance(item[1], datetime.datetime):
					update_dict['date'] = update_dict['timestamp'].strftime('%Y-%m-%d')
					update_dict['timestamp'] = update_dict['timestamp'].strftime('%H:%M')
			print update_dict
			blog_dict['updates'].append(update_dict)

		blog_dict['updates'] = sorted(blog_dict['updates'], key=lambda update: update['timestamp'], reverse=True)

		for item in blog_dict.items():
			if isinstance(item[1], ObjectId):
				blog_dict['id'] = item[1].__str__()
				blog_dict.pop(item[0])

		return json.dumps(blog_dict)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)
