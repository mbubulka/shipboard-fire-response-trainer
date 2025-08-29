"""
Simple HTTP server for DCA assessment
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
import sys
from urllib.parse import parse_qs, urlparse

# Add src directory to path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'test_dqn'))

from dca_assessment_manager import DCAAssessmentManager
from test_dqn.dca_response_evaluator import SimpleResponseEvaluator

# Initialize our assessment system
assessment_manager = DCAAssessmentManager()
evaluator = SimpleResponseEvaluator()

class DCAHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        """Serve static files"""
        if self.path == '/':
            self.path = '/comprehensive.html'
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        """Handle API requests"""
        if self.path == '/api/evaluate':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            # Get the current question
            question = assessment_manager.get_current_question()
            if not question:
                self._send_json({'error': 'No active question'}, 404)
                return

            # Submit and evaluate the answer
            response_data = assessment_manager.submit_answer(
                data['selectedAnswer'],
                data['responseTime']
            )

            # Get DQN evaluation
            evaluation = evaluator.evaluate_response(
                question.scenario,
                response_data,
                {'phase': question.scenario}
            )

            self._send_json(evaluation)
        else:
            self.send_error(404, "Not Found")

    def _send_json(self, data, status=200):
        """Helper to send JSON response"""
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

if __name__ == '__main__':
    server = HTTPServer(('localhost', 5000), DCAHandler)
    print('Starting server at http://localhost:5000')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down server')
        server.server_close()
