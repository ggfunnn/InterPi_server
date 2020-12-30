from flask_api import FlaskAPI
from interpi_server import interpi_server
import os

# start button daemon
path = os.path.dirname(os.path.realpath(__file__))
os.system('python3 ' + path + '/button_daemon.py')

app = FlaskAPI(__name__)
api = interpi_server.Interpi_server()

from interpi_server import routes
