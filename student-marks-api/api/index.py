import json
import os
from http.server import BaseHTTPRequestHandler

def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, '..', 'q-vercel-python.json')
    with open(json_path) as f:
        return json.load(f)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        query = self.path.split('?')[-1]
        params = dict(p.split('=') for p in query.split('&') if '=' in p)
        names = params.get('name', '').split(',') if 'name' in params else []
        
        data = load_data()
        marks = [data.get(name, None) for name in names]
        
        self.wfile.write(json.dumps({"marks": marks}).encode())
