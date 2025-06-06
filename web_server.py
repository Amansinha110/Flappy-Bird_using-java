#!/usr/bin/env python3
import http.server
import socketserver
import os
import subprocess
import threading
import time

class GameHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/run_game.html'
        elif self.path == '/run-game':
            # Try to run the Java game
            try:
                # Set display and run the game
                env = os.environ.copy()
                env['DISPLAY'] = ':1'
                subprocess.Popen(['java', 'App'], cwd='/workspace/Flappy-Bird_using-java', env=env)
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'''
                <html>
                <head><title>Game Started</title></head>
                <body>
                <h1>Flappy Bird Game Started!</h1>
                <p>The game has been launched. If you're running this locally with X11 forwarding, you should see the game window.</p>
                <p><a href="/">Back to main page</a></p>
                </body>
                </html>
                ''')
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f'<html><body><h1>Error starting game: {str(e)}</h1><p><a href="/">Back</a></p></body></html>'.encode())
                return
        elif self.path.endswith('.java'):
            # Serve Java source files
            try:
                file_path = '/workspace/Flappy-Bird_using-java' + self.path
                with open(file_path, 'r') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.send_header('Content-Disposition', f'attachment; filename="{os.path.basename(self.path)}"')
                self.end_headers()
                self.wfile.write(content.encode())
                return
            except FileNotFoundError:
                pass
        
        return super().do_GET()

def start_virtual_display():
    """Start virtual display for the Java application"""
    try:
        # Kill any existing Xvfb processes
        subprocess.run(['pkill', 'Xvfb'], stderr=subprocess.DEVNULL)
        time.sleep(1)
        
        # Start new Xvfb
        subprocess.Popen(['Xvfb', ':1', '-screen', '0', '800x600x24'], 
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)
        print("Virtual display started on :1")
    except Exception as e:
        print(f"Error starting virtual display: {e}")

if __name__ == "__main__":
    # Change to the game directory
    os.chdir('/workspace/Flappy-Bird_using-java')
    
    # Start virtual display
    start_virtual_display()
    
    # Start web server
    PORT = 12000
    
    with socketserver.TCPServer(("0.0.0.0", PORT), GameHandler) as httpd:
        print(f"🎮 Flappy Bird Game Server running at:")
        print(f"   Local: http://localhost:{PORT}")
        print(f"   External: https://work-1-exogdzarrhwsqpbp.prod-runtime.all-hands.dev")
        print(f"\n📁 Serving from: {os.getcwd()}")
        print(f"🐦 Java game files ready!")
        print(f"\nPress Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")
            # Clean up
            subprocess.run(['pkill', 'Xvfb'], stderr=subprocess.DEVNULL)
            subprocess.run(['pkill', 'java'], stderr=subprocess.DEVNULL)