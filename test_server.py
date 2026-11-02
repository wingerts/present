#!/usr/bin/env python3
"""
Simple test server to simulate rtl-tcp server for development purposes.
This script demonstrates how the websocket connection would work with actual rtl-tcp data.
"""

import asyncio
import websockets
import struct
import random
import time
import threading
import signal
import sys

# Simulated RTL-SDR data
class MockRTLSDRServer:
    def __init__(self, host='localhost', port=1234):
        self.host = host
        self.port = port
        self.running = False
        
    async def handle_client(self, websocket, path):
        print(f"Client connected from {websocket.remote_address}")
        try:
            while self.running:
                # Simulate spectrum data (1024 samples)
                # Each sample is 1 byte (0-255) representing signal strength
                # In a real implementation, this would be actual RTL-SDR data
                data = bytes([random.randint(0, 255) for _ in range(1024)])
                await websocket.send(data)
                await asyncio.sleep(0.1)  # Send data every 100ms
        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected")
        except Exception as e:
            if self.running:  # Only print error if we're still running
                print(f"Error: {e}")
    
    async def start(self):
        self.running = True
        server = await websockets.serve(self.handle_client, self.host, self.port)
        print(f"Mock RTL-SDR server running on {self.host}:{self.port}")
        print("Press Ctrl+C to stop")
        await server.wait_closed()
    
    def stop(self):
        self.running = False

# For demonstration, let's also create a simple HTTP server to serve our HTML file
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class SimpleHTTPServer:
    def __init__(self, port=8000):
        self.port = port
        self.httpd = None
        
    def start(self):
        # Change to the current directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        handler = SimpleHTTPRequestHandler
        self.httpd = HTTPServer(('', self.port), handler)
        print(f"HTTP server running on port {self.port}")
        print("Navigate to http://localhost:8000 to view the RTL-SDR interface")
        print("Press Ctrl+C to stop")
        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nHTTP server stopped")

def signal_handler(sig, frame):
    print('\nShutting down servers...')
    sys.exit(0)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='RTL-SDR Test Server')
    parser.add_argument('--mode', choices=['websocket', 'http', 'both'], 
                       default='both', help='Mode to run server in')
    parser.add_argument('--ws-port', type=int, default=1234, help='WebSocket port')
    parser.add_argument('--http-port', type=int, default=8000, help='HTTP server port')
    
    args = parser.parse_args()
    
    # Setup signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    if args.mode in ['websocket', 'both']:
        # Start WebSocket server in a separate thread
        ws_server = MockRTLSDRServer(port=args.ws_port)
        ws_thread = threading.Thread(target=asyncio.run, args=(ws_server.start(),))
        ws_thread.daemon = True
        ws_thread.start()
        print("WebSocket server started in background")
    
    if args.mode in ['http', 'both']:
        # Start HTTP server
        http_server = SimpleHTTPServer(port=args.http_port)
        http_server.start()

if __name__ == "__main__":
    main()