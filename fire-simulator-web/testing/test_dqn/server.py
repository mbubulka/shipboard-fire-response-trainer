"""
Simple HTTP server for DCA assessment
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import time
from dca_scenario_states import DCAAssessmentManager


# Initialize our assessment system
assessment_manager = DCAAssessmentManager()

# Track response times
response_times = {}


class DCAHandler(SimpleHTTPRequestHandler):
    def _send_json(self, data, status=200):
        """Helper method to send JSON responses"""
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = json.dumps(data).encode('utf-8')
        self.wfile.write(response)
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        print(f"GET request: {self.path}")
        
        if self.path == '/api/scenario':
            scenario = assessment_manager.get_current_scenario()
            if scenario:
                # Record start time for this scenario
                response_times[scenario.scenario_id] = time.time()
                
                fire_state = scenario.fire_state
                response = {
                    'id': scenario.scenario_id,
                    'description': scenario.description,
                    'options': scenario.options,
                    'state': {
                        'class': fire_state.class_,
                        'phase': fire_state.phase,
                        'location': fire_state.location,
                        'intensity': fire_state.intensity
                    }
                }
                print(f"Sending scenario: {response}")
                self._send_json(response)
                return
            else:
                self._send_json({'error': 'No more scenarios'}, 404)
                return
        
        if self.path == '/':
            self.path = '/comprehensive.html'
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        """Handle POST requests"""
        print(f"POST request: {self.path}")
        
        if self.path == '/api/evaluate':
            try:
                # Read POST data
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                print(f"Received evaluation data: {data}")

                # Get current scenario
                scenario = assessment_manager.get_current_scenario()
                if not scenario:
                    self._send_json({'error': 'No active scenario'}, 404)
                    return

                # Get selected option
                decision = data.get('selectedOption')
                if decision is None:
                    decision = data.get('decision')
                if decision is None:
                    self._send_json({'error': 'No option selected'}, 400)
                    return

                # Submit decision and get consequences
                result = assessment_manager.submit_decision(decision)
                
                # Build response with new scenario
                next_scenario = assessment_manager.get_current_scenario()
                response = {
                    'consequences': result,
                    'next_scenario': {
                        'id': next_scenario.scenario_id,
                        'description': next_scenario.description,
                        'options': next_scenario.options,
                        'state': {
                            'class': next_scenario.fire_state.class_,
                            'phase': next_scenario.fire_state.phase,
                            'location': next_scenario.fire_state.location,
                            'intensity': next_scenario.fire_state.intensity
                        }
                    } if next_scenario else None
                }
                
                # Calculate scores from consequences
                score = result.get('effectiveness', 0)
                feedback = []
                
                if result.get('state_changes'):
                    feedback.extend(result['state_changes'])
                if result.get('new_risks'):
                    for risk in result['new_risks']:
                        feedback.append(f"Warning: {risk}")

                response['evaluation'] = {
                    'score': score,
                    'feedback': feedback,
                }

                print(f"Sending response: {response}")
                self._send_json(response)
                
                # Calculate decision score based on protocol and safety
                decision_score = (protocol_score + safety_score) / 2
                
                # Generate feedback based on consequences
                feedback = []
                if consequences.get('state_changes'):
                    feedback.extend(consequences['state_changes'])
                if consequences.get('new_risks'):
                    feedback.extend([f"Warning: {risk}" for risk in consequences['new_risks']])
                if not feedback:
                    feedback = ["Action taken, monitoring situation"]

                response = {
                    'evaluation': {
                        'score': score,
                        'confidence': 0.9,  # High AI confidence for fire scenarios
                        'feedback': ' '.join(feedback),
                        'details': {
                            'protocol_score': protocol_score,
                            'safety_score': safety_score,
                            'decision_score': decision_score
                        }
                    }
                }
                self._send_json(response)
            except Exception as e:
                print(f"Error processing request: {str(e)}")
                self._send_json({'error': str(e)}, 500)
            return

        # Handle unknown POST endpoints
        self._send_json({'error': 'Endpoint not found'}, 404)


def main():
    server = HTTPServer(('localhost', 8000), DCAHandler)
    print('Starting server at http://localhost:8000')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down server')
        server.server_close()


if __name__ == '__main__':
    main()
