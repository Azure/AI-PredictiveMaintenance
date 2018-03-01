from flask import Flask, render_template, Response, request
import numpy as np
from threading import Thread
from azure.storage.blob import PageBlobService
from azure.storage.blob import BlockBlobService
# from flask_socketio import SocketIO, send, emit
#from time import sleep
from datetime import datetime
from flask_sockets import Sockets
# https://coderwall.com/p/q2mrbw/gevent-with-debug-support-for-flask
from werkzeug.serving import run_with_reloader
from werkzeug.debug import DebuggedApplication
from gevent import pywsgi, sleep, Timeout
from geventwebsocket.handler import WebSocketHandler
from azure.storage.table import TableService, Entity, TablePermissions

from flask_breadcrumbs import Breadcrumbs, register_breadcrumb

# from gevent import monkey
# monkey.patch_all()

app = Flask(__name__)
app.debug = True
# sockets = Sockets(app)

# Initialize Flask-Breadcrumbs
Breadcrumbs(app=app)

ACCOUNT_NAME = "stgw74e5yvuyvfs2"
ACCOUNT_KEY = "CKXt/8SpgY6JHfVwBQUkwBCDeBKyJzQV10sgut3L4dS/bjKlSxQsPedHkrI7td8I0NBWJoQOSkcChGo1MIf9Cw=="
CONTAINER_NAME = "simulation"

table_service = TableService(account_name=ACCOUNT_NAME, account_key=ACCOUNT_KEY)


@app.route('/')
@register_breadcrumb(app, '.', 'Home')
def home():    
    return render_template('home.html')

@app.route('/equipment')
@register_breadcrumb(app, '.equipment', 'Equipment')
def equipment():
    assets = table_service.query_entities('equipment')
    return render_template('equipment.html', assets = assets)


def view_asset_dlc(*args, **kwargs):
    kind = request.view_args['kind']
    tag = request.view_args['tag']
    return [
        {'text': kind, 'url': '/equipment/{0}'.format(kind)},
        {'text': tag, 'url': '/equipment/{0}/{1}'.format(kind, tag)}]


@app.route('/equipment/<kind>/<tag>')
@register_breadcrumb(app, '.equipment.asset', '', dynamic_list_constructor=view_asset_dlc)
def equipment_asset(kind, tag):
    asset = table_service.get_entity('equipment', kind, tag)
    print(asset)
    return render_template('asset.html', assets = [asset])

if __name__ == "__main__":
    table_service.create_table('equipment')

    asset = {'PartitionKey': 'pm1', 'RowKey': 'pm1-353', 'Installed': datetime(2009, 10, 10), 'Model': 'M009'}
    table_service.insert_or_merge_entity('equipment', asset)

    asset = {'PartitionKey': 'pm1', 'RowKey': 'pm1-354', 'Installed': datetime(2001, 1, 13), 'Model': 'M009'}
    table_service.insert_or_merge_entity('equipment', asset)

    app.run('0.0.0.0', 8000, debug=True)
