from flask import Flask
import os
from app.api import api_bp
from app.client import client_bp
import logging
basedir = os.path.abspath(os.path.dirname(__file__))

logging.info(basedir)
app = Flask(__name__, static_url_path='')
setattr(app, 'static_folder', basedir+'\\client\\app\\dist')
setattr(app, 'template_folder', basedir+'\\client\\app\\dist')
app.register_blueprint(api_bp)
app.register_blueprint(client_bp)

from . import config
app.logger.info('>>> {}'.format(app.config['MODE']))
