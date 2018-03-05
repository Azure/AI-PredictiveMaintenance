import numpy as np
import os
from flask import Flask, render_template, Response, request
from threading import Thread
from azure.storage.blob import PageBlobService
from azure.storage.blob import BlockBlobService
from datetime import datetime
from azure.storage.table import TableService, Entity, TablePermissions
from flask_breadcrumbs import Breadcrumbs, register_breadcrumb

app = Flask(__name__)
app.debug = True

# Initialize Flask-Breadcrumbs
Breadcrumbs(app=app)

STORAGE_ACCOUNT_NAME = os.environ['STORAGE_ACCOUNT_NAME']
STORAGE_ACCOUNT_KEY = os.environ['STORAGE_ACCOUNT_KEY']

table_service = TableService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)

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
