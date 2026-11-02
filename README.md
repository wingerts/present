# RTL-SDR Spectrum and Waterfall Viewer

This project provides a web-based interface to visualize live spectrum and waterfall data from an RTL-SDR device connected to a rtl-tcp server.

## Features
- Real-time spectrum display (frequency vs amplitude)
- Waterfall visualization showing frequency over time
- Responsive design that works on different screen sizes
- WebSocket communication with rtl-tcp server
- Interactive controls for server address, port, frequency, and gain

## Requirements
- RTL-SDR device (RTL2832U based)
- rtl-tcp server running on the same machine or network
- Web browser with WebSocket support

## How to Use
1. Start rtl-tcp server on your machine:
   ```
   rtl_tcp -p 1234 -f 100000000
   ```
   (This starts rtl-tcp on port 1234, center frequency 100 MHz)

2. Open the index.html file in a web browser (you can use any modern browser)

3. Enter the server address and port in the controls:
   - Server Address: localhost (or your server's IP)
   - Port: 1234 (or whatever port you configured)

4. Click "Connect" to establish connection

5. Adjust frequency and gain settings as needed

## Testing
For development/testing purposes, the web interface includes simulated data.
In a real setup, the interface will connect to the actual rtl-tcp server to receive live data.

## File Structure
- `index.html`: Main HTML file with the visualization
- `test_server.py`: Python script to simulate rtl-tcp server for testing
- `README.md`: This file

## How to Test the Implementation

### Option 1: Using Real RTL-SDR Hardware
1. Connect your RTL-SDR device to your computer
2. Install rtl-sdr tools: `sudo apt-get install rtl-sdr`
3. Start rtl-tcp server:
   ```
   rtl_tcp -p 1234 -f 100000000
   ```
4. Open `index.html` in a web browser and connect to localhost:1234

### Option 2: Using the Test Server
1. Run the test server: `python test_server.py --mode both`
2. Open a web browser and navigate to `http://localhost:8000`
3. The interface will automatically connect to the mock server

## Implementation Details

### Spectrum Visualization
- Shows frequency spectrum from RTL-SDR
- Color-coded amplitude representation
- Frequency labels and grid lines for reference

### Waterfall Visualization  
- Shows frequency activity over time
- Color gradient from blue (low) to red (high) intensity
- History of recent spectrum readings

### WebSocket Communication
- Connects to rtl-tcp server via WebSocket
- Receives binary data for spectrum analysis
- Handles connection status and error conditions

## Browser Compatibility
This implementation works in modern browsers that support:
- HTML5 Canvas API
- WebSocket API
- JavaScript ES6 features

## Troubleshooting
- If you get connection errors, ensure rtl-tcp server is running
- Check that the server address and port match your configuration
- Make sure your firewall isn't blocking the connection
- For CORS issues, consider using a local HTTP server
