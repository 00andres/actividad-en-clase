#!/usr/bin/env python3
"""
Servidor HTTP simple para servir la visualización de One Piece Storytelling
"""
import http.server
import socketserver
import os
from pathlib import Path

PORT = 8000
os.chdir(Path(__file__).parent / 'static')

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, format, *args):
        print(f'[{self.log_date_time_string()}] {format%args}')

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║  🏴‍☠️  One Piece - Storytelling Visualizer                  ║
║                                                              ║
║  Servidor ejecutándose en: http://localhost:{PORT}          ║
║  Presiona Ctrl+C para detener                               ║
╚══════════════════════════════════════════════════════════════╝
        """)
        httpd.serve_forever()
