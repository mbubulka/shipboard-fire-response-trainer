#!/usr/bin/env python3
"""
Production WSGI server for DCA Feedback API
Uses Waitress for production-grade serving
"""

from waitress import serve
from feedback_api import app
import os

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5002))
    
    print("🚀 Starting DCA Feedback API Production Server")
    print(f"📡 Listening on port {port}")
    print("💻 Using Waitress WSGI server")
    
    # Start Waitress server
    serve(app, host='0.0.0.0', port=port, threads=4)
