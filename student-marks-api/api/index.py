from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
from os import path

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Get query parameters
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        
        # Get names from query
        names = params.get('name', [])
        
        # Load marks data
        file_path = path.join(path.dirname(__file__), '..', 'q-vercel-python.json')
        with open(file_path) as f:
            data = json.load(f)
        
        # Get marks for requested names
        marks = []
        for name in names:
            marks.append(data.get(name, None))
        
        # Prepare response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Enable CORS
        self.end_headers()
        
        response = {
            "marks": marks
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
        return