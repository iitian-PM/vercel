from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
from os import path

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
            
            # Load marks data
            file_path = path.join(path.dirname(__file__), '..', 'q-vercel-python.json')
            with open(file_path) as f:
                data = json.load(f)
            
            # Get marks
            marks = [data.get(name, None) for name in names]
            
            response = {"marks": marks}
        except Exception as e:
            response = {"error": str(e)}
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
