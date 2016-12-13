
#! /usr/bin/python

import os
from flask import Flask
import temporary_pb2

app = Flask(__name__)

APPS_DIR='/home/nagash/workspace-android/AppWeb/CentralServer/ManagedApps'



config = {
  'user': 'root',
  'password': 'root',
  'host': '127.0.0.1',
  'database': 'webapp_db',
  'raise_on_warnings': True,
}


#androidAppList=temporary_pb2.AppList()

@app.route('/')
def hello_world2():
	iosAppList=temporary_pb2.AppList()
	appNames=os.listdir(APPS_DIR)
	androidAppList=temporary_pb2.AppList()
	for appName in appNames:
		appPath = APPS_DIR + '/' + appName
		if os.path.isfile(appPath + '/' + 'index.android.bundle' ):
			app = androidAppList.app.add()
			app.appName=appName
		if os.path.isfile(appPath + '/' + 'index.ios.bundle' ):
			app = iosAppList.app.add()
			app.appName=appName


	return androidAppList.SerializeToString()

