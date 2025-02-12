import os
from flask import Flask, render_template, jsonify
import psutil
from flask_socketio import SocketIO


app = Flask(__name__, template_folder='frontend', static_folder='static')

@app.route('/')
def home():
    return render_template('index.html')

def get_perf_values():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    network_usage_dl = psutil.net_io_counters().bytes_recv
    network_usage_ul = psutil.net_io_counters().bytes_sent
    if network_usage_dl > 1000000:
        network_usage_dl = str(round(network_usage_dl / 1000000/8)) + ' MO'
    elif network_usage_dl > 1000:
        network_usage_dl = str(round(network_usage_dl / 1000/8)) + ' KO'
    elif network_usage_dl > 1:
        network_usage_dl = str(round(network_usage_dl / 8)) + ' O'
    else:
        network_usage_dl = "No connexion"

    if network_usage_ul > 1000000:
        network_usage_ul = str(round(network_usage_ul / 1000000/8)) + ' MO'
    elif network_usage_ul > 1000:
        network_usage_ul = str(round(network_usage_ul / 1000/8)) + ' KO'
    elif network_usage_ul > 1:
        network_usage_ul = str(round(network_usage_ul / 8)) + ' O'
    else:
        network_usage_ul = "No connexion"

    return cpu_usage, ram_usage, network_usage_dl, network_usage_ul

@app.route('/perf')
def get_perf_usage():   
    cpu_usage, ram_usage, network_usage_dl, network_usage_ul = get_perf_values()
    return render_template('perf.html', cpu_usage=cpu_usage, ram_usage=ram_usage, network_usage_dl=network_usage_dl, network_usage_ul=network_usage_ul)

@app.route('/get_usage')
def get_usage():
    """Retourne les données en JSON."""
    cpu_usage, ram_usage, network_usage_dl, network_usage_ul = get_perf_values()
    data = {
        "cpu_usage": cpu_usage,
        "ram_usage": ram_usage,
        "network_usage_dl": network_usage_dl,
        "network_usage_ul": network_usage_ul,
    }
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)
