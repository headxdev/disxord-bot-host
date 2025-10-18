from flask import Flask, send_from_directory, jsonify
import os
from pathlib import Path
from server.auth_routes import auth_bp

ROOT = Path(__file__).resolve().parents[1]  # Adjusted to correct project root
app = Flask(__name__, static_folder=str(ROOT / 'frontend'))

# Secret key is required for session management
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# Register the authentication blueprint
app.register_blueprint(auth_bp)


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})



# Info endpoint for network and install info
@app.route('/info')
def info():
    wlan_ip = os.environ.get('WLAN_IP', '127.0.0.1')
    public_ip = os.environ.get('PUBLIC_IP', 'unbekannt')
    return jsonify({
        'wlan_ip': wlan_ip,
        'public_ip': public_ip
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
