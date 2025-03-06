import os
from flask import Flask, render_template, jsonify
import psutil
from flask_socketio import SocketIO

app = Flask(__name__, template_folder='frontend', static_folder='static')

@app.route('/')
def home():
    return render_template('index.html')

prev_net_io = psutil.net_io_counters()

def get_perf_values():
    """
    Retrieves the current performance metrics of the system, including CPU, RAM, and network usage.

    Returns:
        tuple: A tuple containing:
            - cpu_usage (float): The CPU usage percentage.
            - ram_usage (float): The RAM usage percentage.
            - network_usage_dl (str): The formatted download network usage as a string with unit (B/s, KB/s, MB/s).
            - network_usage_ul (str): The formatted upload network usage as a string with unit (B/s, KB/s, MB/s).
    """
    global prev_net_io

    # Récupération de l'utilisation CPU et RAM
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent

    # Récupération des informations réseau actuelles
    net_io_current = psutil.net_io_counters()

    # Calcul du débit de téléchargement et d'upload en octets par seconde
    network_usage_dl = net_io_current.bytes_recv - prev_net_io.bytes_recv
    network_usage_ul = net_io_current.bytes_sent - prev_net_io.bytes_sent

    # Mise à jour des valeurs précédentes
    prev_net_io = net_io_current

    # Formatage du débit de téléchargement
    if network_usage_dl > 1000000:
        network_usage_dl = str(round(network_usage_dl / 1000000)) + ' MB/s'
    elif network_usage_dl >= 1000:
        network_usage_dl = str(round(network_usage_dl / 1000)) + ' KB/s'
    elif network_usage_dl < 1000:
        network_usage_dl = "< 1 KB/s" 

    # Formatage du débit d'upload
    if network_usage_ul > 1000000:
        network_usage_ul = str(round(network_usage_ul / 1000000)) + ' MB/s'
    elif network_usage_ul >= 1000:
        network_usage_ul = str(round(network_usage_ul / 1000)) + ' KB/s'
    elif network_usage_ul < 1000:
        network_usage_ul = "< 1 KB/s"

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

@app.route('/settings')
def settings():
    return render_template('settings.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port, host='0.0.0.0')
