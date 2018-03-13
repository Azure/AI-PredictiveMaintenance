import numpy as np
from flask import Flask, render_template, Response, request
from threading import Thread
from azure.storage.blob import PageBlobService
from azure.storage.blob import BlockBlobService
from datetime import datetime
from azure.storage.table import TableService, Entity, TablePermissions
from flask_breadcrumbs import Breadcrumbs, register_breadcrumb
import sys, os, time, glob
import aztk.models
import aztk.spark
import json
from aztk.error import AztkError

app = Flask(__name__)
app.debug = True

# Initialize Flask-Breadcrumbs
Breadcrumbs(app=app)

BATCH_ACCOUNT_NAME = os.environ['BATCH_ACCOUNT_NAME']
BATCH_ACCOUNT_KEY = os.environ['BATCH_ACCOUNT_KEY']
BATCH_SERVICE_URL = os.environ['BATCH_ACCOUNT_URL']
STORAGE_ACCOUNT_SUFFIX = 'core.windows.net'
STORAGE_ACCOUNT_NAME = os.environ['STORAGE_ACCOUNT_NAME']
STORAGE_ACCOUNT_KEY = os.environ['STORAGE_ACCOUNT_KEY']
TELEMETRY_CONTAINER_NAME = 'telemetry'
IOT_HUB_NAME = os.environ['IOT_HUB_NAME']

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

@app.route('/aztkIns')
@register_breadcrumb(app, '.aztkIns', 'AZTK Instructions')
def aztkIns():
    secrets_confg = aztk.spark.models.SecretsConfiguration(
    shared_key=aztk.models.SharedKeyConfiguration(
        batch_account_name = BATCH_ACCOUNT_NAME,
        batch_account_key = BATCH_ACCOUNT_KEY,
        batch_service_url = BATCH_SERVICE_URL,
        storage_account_name = STORAGE_ACCOUNT_NAME,
        storage_account_key = STORAGE_ACCOUNT_KEY,
        storage_account_suffix = STORAGE_ACCOUNT_SUFFIX
    ),

    ssh_pub_key=""
    )

    # create a client
    client = aztk.spark.Client(secrets_confg)
    try:
        cluster = client.get_cluster(cluster_id="predictive-maintenance")

        node_count = '{}'.format(cluster.total_current_nodes)
        cluster_info = ""

        cluster_info = cluster_info.join("Cluster         {}".format( cluster.id))
        cluster_info = cluster_info.join("------------------------------------------")
        cluster_info = cluster_info.join("State:          {}".format(cluster.visible_state))
        cluster_info = cluster_info.join("Node Size:      {}".format(cluster.vm_size))
        cluster_info = cluster_info.join("Nodes:          {}".format(node_count))
        cluster_info = cluster_info.join("| Dedicated:    {}".format(cluster.current_dedicated_nodes))
        cluster_info = cluster_info.join("| Low priority: {}".format(cluster.current_low_pri_nodes))
        cluster_info = cluster_info.join("")

        print_format = '|{:^36}| {:^19} | {:^21}| {:^10} | {:^8} |'
        print_format_underline = '|{:-^36}|{:-^21}|{:-^22}|{:-^12}|{:-^10}|'
        cluster_info = cluster_info.join(print_format.format("Nodes", "State", "IP:Port", "Dedicated", "Master"))
        cluster_info = cluster_info.join(print_format_underline.format('', '', '', '', ''))
    
        for node in cluster.nodes:
            remote_login_settings = client.get_remote_login_settings(cluster.id, node.id)
            cluster_info = cluster_info.join(
            print_format.format(
                node.id,
                node.state.value,
                '{}:{}'.format(remote_login_settings.ip_address, remote_login_settings.port),
                "*" if node.is_dedicated else '',
                '*' if node.id == cluster.master_node_id else '')
            )
        cluster_info = cluster_info.join('')

    except:
        cluster_info = "Cluster provisioning"

    assets = os.environ['WEBSITE_SITE_NAME']
    return render_template('aztkIns.html', assets = assets, cluster_info = cluster_info)

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
