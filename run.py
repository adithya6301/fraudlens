"""FraudLens Launcher Script
Starts the FastAPI backend and serves the interactive fraud investigation web interface.
Includes automated port conflict detection.
"""

import socket
import argparse
import uvicorn

def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0

def find_available_port(start_port: int = 8000, max_attempts: int = 10, host: str = "127.0.0.1") -> int:
    for port in range(start_port, start_port + max_attempts):
        if not is_port_in_use(port, host):
            return port
    return start_port

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run FraudLens Agentic AI Platform")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the web server on (default: 8000)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host address (default: 127.0.0.1)")
    args = parser.parse_args()

    selected_port = args.port
    if is_port_in_use(selected_port, args.host):
        alt_port = find_available_port(selected_port + 1, host=args.host)
        print(f"[!] Notice: Port {selected_port} is busy. Automatically switching to: {alt_port}")
        selected_port = alt_port

    print("=" * 72)
    print("  FRAUDLENS: An Agentic AI System for Intelligent Fraud Investigation")
    print("=" * 72)
    print(f"  Web Dashboard URL: http://{args.host}:{selected_port}")
    print("  Press Ctrl+C to stop the server.")
    print("=" * 72)

    uvicorn.run("app.main:app", host=args.host, port=selected_port, reload=False)
