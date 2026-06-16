#!/usr/bin/env python3
"""
MoreLinks PWA Server
Python HTTP server for Android PWA
Run: python server.py
"""

import http.server
import socketserver
import os
from pathlib import Path

PORT = 8080
DIRECTORY = Path(__file__).parent.absolute()


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)
    
    def end_headers(self):
        # Add CORS headers for mobile
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Service-Worker-Allowed', '/')
        super().end_headers()
    
    def do_GET(self):
        # Serve manifest.json with correct content-type
        if self.path == '/manifest.json':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            with open(DIRECTORY / 'manifest.json', 'rb') as f:
                self.wfile.write(f.read())
            return
        
        # Serve service worker
        if self.path == '/sw.js':
            self.send_response(200)
            self.send_header('Content-Type', 'application/javascript')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            with open(DIRECTORY / 'sw.js', 'rb') as f:
                self.wfile.write(f.read())
            return
        
        # Default to index.html for SPA routing
        if not os.path.splitext(self.path)[1]:
            self.path = '/index.html'
        
        return super().do_GET()


def main():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"""
╔════════════════════════════════════════════════════╗
║                                            ║
║   🔗 MoreLinks PWA Server                   ║
║                                            ║
║   📱 Server avviato su http://localhost:{PORT}   ║
║   🌐 Per accesso esterno: http://0.0.0.0:{PORT}  ║
║                                            ║
║   📋 Apri nel browser:                     ║
║   http://localhost:{PORT}                      ║
║                                            ║
║   📲 Per Android PWA:                       ║
║   1. Apri http://<tuo-ip>:{PORT}             ║
║   2. Chrome → Menu → Aggiungi alla Home    ║
║                                            ║
║   🛑 Ctrl+C per fermare                    ║
║                                            ║
╚════════════════════════════════════════════════════╝
        """)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server fermato!")


if __name__ == "__main__":
    main()
