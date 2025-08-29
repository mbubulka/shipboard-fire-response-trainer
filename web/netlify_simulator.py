#!/usr/bin/env python3
"""
Local Netlify Function Simulator
Tests the DCA evaluation function locally before deployment
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import os
import sys

class NetlifySimulator(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        """Send CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def do_OPTIONS(self):
        """Handle preflight CORS requests"""
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        """Serve static files"""
        # Parse the path
        path = self.path.lstrip('/')
        
        # Default to index.html
        if not path or path == '/':
            path = 'bubulkaanalytics-site/index.html'
        elif not path.startswith('bubulkaanalytics-site/'):
            path = f'bubulkaanalytics-site/{path}'
        
        try:
            # Determine content type
            if path.endswith('.html'):
                content_type = 'text/html'
            elif path.endswith('.js'):
                content_type = 'application/javascript'
            elif path.endswith('.css'):
                content_type = 'text/css'
            else:
                content_type = 'text/plain'
            
            # Read and serve the file
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
            
        except FileNotFoundError:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(b'File not found')
        except Exception as e:
            print(f"Error serving {path}: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(f'Server error: {e}'.encode('utf-8'))
    
    def do_POST(self):
        """Handle API calls"""
        if self.path.startswith('/api/dca-evaluate'):
            self._handle_dca_evaluate()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"error": "API endpoint not found"}).encode())
    
    def _handle_dca_evaluate(self):
        """Simulate the Netlify dca-evaluate function"""
        try:
            # Read the request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            print(f"📥 DCA Evaluate Request: {data}")
            
            # Simulate the evaluation logic from the Netlify function
            evaluation = self._simulate_dca_evaluation(data)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self._send_cors_headers()
            self.end_headers()
            
            response = json.dumps(evaluation)
            print(f"📤 DCA Evaluate Response: {response}")
            self.wfile.write(response.encode())
            
        except Exception as e:
            print(f"❌ Error in DCA evaluation: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def _simulate_dca_evaluation(self, data):
        """Simulate the DCA evaluation logic"""
        # Default values
        response_time_ms = data.get('response_time_ms', 5000)
        is_correct = data.get('is_correct', False)
        scenario = data.get('scenario', 'Unknown')
        
        # Calculate time score (optimal: 3-8 seconds)
        response_time_sec = response_time_ms / 1000
        if response_time_sec < 2:
            time_score = 0.6  # Too fast
        elif response_time_sec <= 5:
            time_score = 1.0  # Optimal
        elif response_time_sec <= 10:
            time_score = 0.8  # Good
        elif response_time_sec <= 20:
            time_score = 0.6  # Acceptable
        else:
            time_score = 0.3  # Too slow
        
        # Protocol score
        protocol_score = 1.0 if is_correct else 0.0
        
        # Safety score
        safety_score = 0.9 if is_correct else 0.3
        if "Safety" in scenario or "Emergency" in scenario:
            safety_score *= 1.1
        
        # Weighted total score
        weights = {"speed": 0.3, "protocol": 0.4, "safety": 0.3}
        total_score = (
            weights["speed"] * time_score +
            weights["protocol"] * protocol_score +
            weights["safety"] * safety_score
        )
        
        # Confidence
        scores = [time_score, protocol_score, safety_score]
        confidence = 1.0 - (max(scores) - min(scores)) / 2
        
        # Feedback
        feedback = []
        if total_score >= 0.8:
            feedback.append("Excellent response! Strong decision-making skills.")
        elif total_score >= 0.6:
            feedback.append("Good response with room for improvement.")
        else:
            feedback.append("Consider reviewing procedures for this scenario.")
        
        if time_score < 0.5:
            feedback.append("Response time could be optimized.")
        
        if protocol_score < 0.5:
            feedback.append("Review standard operating procedures.")
        
        return {
            "score": round(total_score, 2),
            "confidence": round(confidence, 2),
            "feedback": " ".join(feedback),
            "details": {
                "time_score": round(time_score, 2),
                "protocol_score": round(protocol_score, 2),
                "safety_score": round(safety_score, 2)
            }
        }

def main():
    print("🧪 Netlify Function Simulator Starting...")
    print("📁 Serving from: bubulkaanalytics-site/")
    print("🔗 API endpoint: /api/dca-evaluate")
    print("🌐 URL: http://localhost:9000")
    print("=" * 50)
    
    server = HTTPServer(('localhost', 9000), NetlifySimulator)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down simulator")
        server.server_close()

if __name__ == '__main__':
    main()
