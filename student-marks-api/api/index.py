import json
import os
from http.server import BaseHTTPRequestHandler

def load_student_data():
    # Get absolute path to JSON file
    here = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(here, '..', 'q-vercel-python.json')
    
    # Verify file exists
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"JSON file not found at {json_path}")
    
    with open(json_path) as f:
        return json.load(f)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Handle all routes
            if self.path.startswith('/api') or self.path == '/':
                self.handle_api_request()
            else:
                self.send_error(404, "Endpoint not found")
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")

    def handle_api_request(self):
        # Get query parameters
        query = self.path.split('?')[-1]
        params = {}
        for param in query.split('&'):
            if '=' in param:
                key, value = param.split('=', 1)
                params[key] = value
        
        # Get names from query
        names = []
        if 'name' in params:
            names = params['name'].split(',')
        
        # Load data and prepare response
        data = load_student_data()
        marks = [data.get(name, None) for name in names]
        
        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"marks": marks}).encode())

# Test handler locally (won't run on Vercel)
if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 8000), handler)
    print("Testing server at http://localhost:8000")
    server.serve_forever()
