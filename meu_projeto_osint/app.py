import os
import base64
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Configuração da pasta de salvamento
UPLOAD_FOLDER = 'static/logs/intruders'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Lista todas as fotos e manda para a página do painel
    fotos = os.listdir(UPLOAD_FOLDER)
    fotos.sort(reverse=True) # Fotos novas primeiro
    return render_template('dashboard.html', fotos=fotos)

@app.route('/security/intruder_capture', methods=['POST'])
def capture():
    try:
        data = request.get_json()
        image_data = data.get('image')
        if image_data:
            header, encoded = image_data.split(",", 1)
            binary_data = base64.b64decode(encoded)
            filename = f"intruder_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            with open(filepath, "wb") as f:
                f.write(binary_data)
            print(f"\033[91m[!] ALERTA: Foto salva em {filename}\033[0m")
            return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
