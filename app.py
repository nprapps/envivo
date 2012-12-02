#!/usr/bin/env python

import datetime
import json
import os

from flask import Flask
from flask import render_template, request
from mongoengine import connect

from models import LiveBlog, LiveBlogUpdate

app = Flask(__name__)

db = connect('apps', username=os.env['APPS_USER'], password=os.env['APPS_PASS'])

@app.route('/live-blog/<live_blog_id>/', methods=['GET', 'POST'])
def live_blog_list(live_blog_id=None):

	if request.method == 'GET':

		if live_blog_id == None:

			for blog in LiveBlog.objects:

				