#!/usr/bin/env python3
"""
Servidor HTTP simple para servir la visualización de One Piece Storytelling
"""
import http.server
import socketserver
import os
from pathlib import Path

# --- CONFIGURACIÓN ---
PORT = 8000

# CORRECCIÓN: Ahora apuntamos al directorio donde está este mismo script (server.py)
# en lugar de buscar una carpeta 'static' que ya no usas.
root_dir = Path(__file__).parent
os.chdir(root_dir)

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Evitar caché para que veas los cambios al instante
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, format, *args):
        # Log limpio en consola
        print(f'[{self.log_date_time_string()}] {format%args}')

if __name__ == '__main__':
    # Configuración para permitir reconexión rápida al puerto si reinicias
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║  🏴‍☠️  One Piece - Storytelling Visualizer                  ║
║                                                              ║
║  Servidor ejecutándose en: http://localhost:{PORT}          ║
║  Directorio raíz: {root_dir}           
║  Presiona Ctrl+C para detener                                ║
╚══════════════════════════════════════════════════════════════╝
        """)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Servidor detenido.")
            httpd.server_close()