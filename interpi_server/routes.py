from interpi_server import app
from interpi_server import api

@app.route('/unlock/', methods=['GET', 'POST'])
def unlock():
    return api.unlock()

@app.route('/lock/', methods=['GET', 'POST'])
def lock():
    return api.lock()

