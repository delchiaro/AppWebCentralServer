from __future__ import print_function # In python 2.7

from flask import Flask, render_template, request, redirect

from werkzeug.utils import secure_filename
import os

from pprint import pprint
import sys

app = Flask(__name__)


config = {
  'user': 'root',
  'password': 'root',
  'host': '127.0.0.1',
  'database': 'webapp_db',
  'raise_on_warnings': True,
}



#UPLOAD_FOLDER = '/home/delchiaro/CentralServer/ManagedApps'
UPLOAD_FOLDER = 'ManagedApps'
PROTOBIN_FILE_NAME = 'webAppProto.protobin'
APPS_DIR=UPLOAD_FOLDER
ANDROID_BUNDLE_FILENAME='index.android.bundle'


import app_pb2
import warnings





# * * * * * * * * INDEX * * * * * * *

@app.route('/', methods = ['GET', 'POST'])
def index_page():
    return render_template('index.html')





@app.route('/manage_webapp')
def listAppsHTML():
    
    appIds=os.listdir(APPS_DIR)
    app_list_android=[]
    app_list_ios=[]
    for appId in appIds:
		
        appPath = APPS_DIR + '/' + appId + '/'

        if os.path.isfile(appPath  + PROTOBIN_FILE_NAME):
            fileProto = open(appPath  + PROTOBIN_FILE_NAME,"r")
            protobin = fileProto.read()
            fileProto.close()
            webApp = app_pb2.WebApp()
            webApp.ParseFromString(protobin)

            if appId != webApp.appId:
                warnings.warn("Nome cartella '"+ appId + "' non coincide con ID app '" + webApp.appId + "'.", RuntimeWarning)
                #ERROR: nome cartella non coincide con ID della applicazione!
            
            if os.path.isfile(appPath + webApp.indexFileAndroid):
                app_list_android.append(webApp)
                
            #if os.path.isfile(appPath + webApp.indexFileIos):
            

    return render_template('webapp_manager.html', app_list=app_list_android)



# * * * * * * * * INSERT APP MODULE * * * * * * *
#
# @app.route('/insert_app', methods = ['GET', 'POST'])
#def insert_app_page():
#    return render_template('appmodule.html')











# * * * * * * * * * * * * * * * * * * * * * * * SEND APP PAGE * * * * * * * * * * * * * * * * * * * * * * *

import re
from operator import xor

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def appId_match(strg, search=re.compile(r'[^A-Z-a-z0-9._]').search):
    return not bool(search(strg))


ALLOWED_EXTENSIONS = set(['bundle'])


	


@app.route('/sendapp', methods = ['GET', 'POST'])
def sendapp_page():
    if request.method == 'POST':
        
        missing_info=[]
        webApp = app_pb2.WebApp()
        if 'appId' not in request.form or request.form['appId']=='':
            missing_info.append('Application Identifier')
        else:
            if appId_match( request.form['appId'] ) == True:
                webApp.appId=request.form['appId']
            else:
                missing_info.append('Application Identifier not valid. Valid chars are only: A-Z  a-z  _ . - ')

        if 'appName' not in request.form or request.form['appName']=='':
            missing_info.append('Application Name')
        else:
            webApp.appName=request.form['appName']
                
        if 'versionCode' not in request.form or request.form['versionCode']=='':
            missing_info.append('Version Code')
        else:
            webApp.versionCode=int(request.form['versionCode'])

        if 'versionName' not in request.form or request.form['versionName']=='':
            missing_info.append('Version Name')
        else:
            webApp.versionName=request.form['versionName']


        # GPS coordinates:
	if 'long' in request.form and request.form['long']!='':
            webApp.long=request.form['long']

	if 'lat' in request.form and request.form['lat']!='':
            webApp.lat=request.form['lat']

	if bool(webApp.lat is None) ^ bool(webApp.long is None):
            missing_info.append('Longitude and Latitude must be filled both or none');

        
        # Eddystone Beacon
        if 'uid_namespace' in request.form and request.form['uid_namespace']!='':
            webApp.beacon.UID_namespace=request.form['uid_namespace']

	if 'uid_instance' in request.form and request.form['uid_instance']!='':
            webApp.beacon.UID_instance=request.form['uid_instance']

        if bool( webApp.beacon.UID_instance is None) ^ bool(webApp.beacon.UID_namespace is None):
            missing_info.append('UID namespace and instance must be filled both or none');

        if 'tlm' in request.form and request.form['tlm']!='':
            webApp.beacon.TLM=request.form['tlm']

        if 'generate_url' in request.form and request.form['generate_url']==True:
            webApp.beacon.URL=webApp.appId
            # url is used to store in the beacon the appId so that the Browser, when is next to the beacon,
            # can connect to the central server and make a request for the app without any other query.
            # We could use this field also to sore the direct URL to the app in a server, but for now we use only
            # the central server to deploy the WebApps.

        # For these properties we always use default protobuf value
        #webApp.indexFile = "index.bundle";
        #webApp.indexFileAndroid = "index.android.bundle";
        #webApp.indexFileIos = "index.ios.bundle";
        #webApp.mainClass = "main";
        #webApp.mainClassAndroid = "main";
        #webApp.mainClassIos = "main";

        file=None
        if request.form['update'] == '0':
            if 'fileAndroid' not in request.files:
                missing_info.append('Bundle for Android')
            file = request.files['fileAndroid']
            if file.filename == '':
                missing_info.append('Bundle for Android')

            if missing_info:
                return render_template('sendfailed.html', cause='Missing Informations', error_list=missing_info)

        print('Hello world!', file=sys.stderr)

        #saveAppToDB() #TODO
        #We use protobuf file instead of db
        FILE_DIR  = UPLOAD_FOLDER   + '/'+ webApp.appId +'/'
        if not os.path.exists(FILE_DIR):
                os.makedirs(FILE_DIR) # se non esiste, creo la cartella
        proto_file = open(FILE_DIR+'/'+PROTOBIN_FILE_NAME,"w")
        proto_file.write(webApp.SerializeToString())
        proto_file.close()


        if file:
            if allowed_file(file.filename)==False:
                return render_template('sendfailed.html', cause='File extension not allowed. Allowed file extension are:', error_list=ALLOWED_EXTENSIONS)

            else:
                filename = secure_filename(ANDROID_BUNDLE_FILENAME)
                FILE_PATH = FILE_DIR + filename
                if not os.path.normpath(FILE_PATH).startswith(UPLOAD_FOLDER):
                    return render_template('sendfailed.html', cause="Error in Path!", error_list="Error in Path!")

                if not os.path.exists(FILE_DIR):
                    os.makedirs(FILE_DIR) # se non esiste, creo la cartella
                file.save(FILE_PATH)


        return render_template('appsended.html')
   
    return 'file not uploaded'
















# LIST FOR ANDROID CLIENT (PROTOBUF CLIENT):

@app.route('/list')
def listApps():
    iosAppList=app_pb2.AppList()
    androidAppList=app_pb2.AppList()
    appIds=os.listdir(APPS_DIR)
    for appId in appIds:

        appPath = APPS_DIR + '/' + appId + '/'

        if os.path.isfile(appPath  + PROTOBIN_FILE_NAME):
            fileProto = open(appPath  + PROTOBIN_FILE_NAME,"r")
            protobin = fileProto.read()
            fileProto.close()
            webApp = app_pb2.WebApp()
            webApp.ParseFromString(protobin)

            if appId != webApp.appId:
                warnings.warn("Nome cartella '"+ appId + "' non coincide con ID app '" + webApp.appId + "'.", RuntimeWarning)
                #ERROR: nome cartella non coincide con ID della applicazione!
            
            if os.path.isfile(appPath + webApp.indexFileAndroid):
                app = androidAppList.app.add()
                app.CopyFrom(webApp)
                
            if os.path.isfile(appPath + webApp.indexFileIos):
                app = iosAppList.app.add()
                app.CopyFrom(webApp)
            
#        if os.path.isfile(appPath + 'index.android.bundle' ):
#            app = androidAppList.app.add()
#            app.appId=appId
#
#        if os.path.isfile(appPath + 'index.ios.bundle' ):
#            app = iosAppList.app.add()
#            app.appId=appId
            
    return androidAppList.SerializeToString()







# DOWNLOAD APP:
from flask import Flask, request, send_from_directory

@app.route('/download/<path:file>')
def downloadApp(file):
	return send_from_directory('../ManagedApps', file)



















































# * * * * * * * * * * * * * * * * * * * * * * * LOGIN PAGE * * * * * * * * * * * * * * * * * * * * * * *
# TODO !!!!
import flask_login
import hashlib, uuid
salt = uuid.uuid4().hex


login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Our mock database.
users = {'foo@bar.tld': {'pw': 'secret'}}

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['pw'] == users[email]['pw']

    return user



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''

    email = flask.request.form['email']
    if request.form['pw'] == users[email]['pw']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id









#def saveAppToDB(string appname):
	# TODO
#	return




if __name__ == "__main__":
    app.run()
