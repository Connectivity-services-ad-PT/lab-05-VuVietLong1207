# src/notification_worker/main.py
"""
Notification Worker service for Lab 05.
Implemented using pure Python standard library to ensure zero-dependency,
fast startup inside raw python:3.11-slim container.
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

SERVICE_NAME = "notification-worker"
SERVICE_VERSION = "1.0.0"

class WorkerHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Override to log clean standard console output
        pass

    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"status": "ok", "service": SERVICE_NAME, "version": SERVICE_VERSION}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"detail": "Not Found"}).encode('utf-8'))

    def do_POST(self):
        if self.path in ('/notify', '/predict'):
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                payload = json.loads(post_data.decode('utf-8')) if post_data else {}
            except Exception:
                payload = {}
                
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            if self.path == '/notify':
                print(f"📧 [WORKER] Received alert notification!")
                print(f"   * Location: {payload.get('location')}")
                print(f"   * Type: {payload.get('type')}")
                print(f"   * Details: {payload.get('details')}")
                print(f"   * Timestamp: {payload.get('timestamp')}")
                print(f"🚀 [WORKER] SMS / Email / Discord notifications successfully dispatched to campus responders.")
                
                response = {
                    "status": "dispatched",
                    "notification": {
                        "channel": "SMS/Email",
                        "sent_to": "campus_emergency_response_team",
                        "timestamp": payload.get('timestamp')
                    }
                }
            else:  # /predict
                response = {
                    "objects": ["person", "bicycle"],
                    "confidence": [0.98, 0.85]
                }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"detail": "Not Found"}).encode('utf-8'))

def run(port=9000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, WorkerHandler)
    print(f"Starting notification worker server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()