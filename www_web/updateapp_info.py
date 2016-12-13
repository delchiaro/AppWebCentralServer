import os
from flask import request, redirect, url_for

from werkzeug.utils import secure_filename
from flask import Blueprint
from flask import current_app as app

sendapp_page = Blueprint('sendapp_page', __name__)

