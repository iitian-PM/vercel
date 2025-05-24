from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        try:
            # Get query parameters
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            names = params.get('name', [])
            
            # Get absolute path to JSON file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(current_dir, '..', 'q-vercel-python.json')
            
            # Load marks data
            with open(json_path) as f:
                data = json.load(f)
            
            # Get marks
            marks = [data.get(name, None) for name in names]
            
            response = {"marks": marks}
        except Exception as e:
            response = {"error": str(e), "path": self.path}
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
