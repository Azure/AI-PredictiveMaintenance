from flask import Flask, render_template, Response
import numpy as np
from threading import Thread
from azure.storage.blob import PageBlobService
from azure.storage.blob import BlockBlobService
# from flask_socketio import SocketIO, send, emit
#from time import sleep
from flask_sockets import Sockets
# https://coderwall.com/p/q2mrbw/gevent-with-debug-support-for-flask
from werkzeug.serving import run_with_reloader
from werkzeug.debug import DebuggedApplication
from gevent import pywsgi, sleep, Timeout
from geventwebsocket.handler import WebSocketHandler
from azure.storage.table import TableService, Entity, TablePermissions

# from gevent import monkey
# monkey.patch_all()

app = Flask(__name__)
app.debug = True
sockets = Sockets(app)

ACCOUNT_NAME = "snsr"
ACCOUNT_KEY = "YU4+T41CmWSRyxuV0v1KMKAGRfaz6PXnbcZK8mjgvV3TKj3jqHvU4T0uvrcQ6YWUuLu84KRCi17vIqlhaq1dRA=="
CONTAINER_NAME = "simulation"

table_service = TableService(account_name=ACCOUNT_NAME, account_key=ACCOUNT_KEY)

@app.route('/')
def hello_world():
      return render_template('index.html')

def stream_thread(ws):
      # ws.on_message = lambda m: print(m)
      bs = PageBlobService(account_name=ACCOUNT_NAME, account_key=ACCOUNT_KEY)
      bbs = PageBlobService(account_name=ACCOUNT_NAME, account_key=ACCOUNT_KEY)      
      n = -1
      chunk = 0
      while not ws.closed:
            # message = ws.receive()
            chunk = (chunk - 1) % 10
            properties = bs.set_sequence_number(CONTAINER_NAME, "buffer", sequence_number_action="max", sequence_number=0)
            new_n = (properties.sequence_number - 2) % 10
            if new_n == n:
                  continue
            n = new_n
            data = bbs.get_blob_to_bytes(CONTAINER_NAME, "buffer", start_range=n * 512 * 32, end_range=(n + 1) * 512 * 32)
            ws.send(data.content[0: 8001 * 2])
            #sleep(0.2)

@sockets.route('/stream')
def stream(ws):
      print('stream')
      thread = Thread(target=stream_thread, args=(ws, ))
      thread.start()
      while not ws.closed:
            with Timeout(0.1, False):
                message = ws.receive()
                if message is not None:                
                  speed = int(message)            
                  device = {'PartitionKey': 'engine', 'RowKey': '1', 'speed': speed * 120}
                  table_service.insert_or_merge_entity('devices', device)
                sleep(1)


def run_server():
    if app.debug:
        application = DebuggedApplication(app)
    else:
        application = app

    server = pywsgi.WSGIServer(('', 5000), application,
                               handler_class=WebSocketHandler)
    server.serve_forever()

if __name__ == "__main__":
    run_with_reloader(run_server)
