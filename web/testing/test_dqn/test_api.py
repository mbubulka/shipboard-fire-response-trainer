"""
API test script for DCA scenario server using urllib
"""
import urllib.request
import urllib.parse
import json


def test_api():
    """Test the DCA scenario API endpoints"""
    base_url = "http://localhost:8000"
    
    # Test 1: Get initial scenario
    print("\nTest 1: Getting initial scenario...")
    try:
        response = urllib.request.urlopen(f"{base_url}/api/scenario")
        scenario = json.loads(response.read().decode('utf-8'))
        print("Success! Got scenario:")
        print(f"ID: {scenario['id']}")
        print(f"Description: {scenario['description']}")
        print(f"State: {scenario['state']}")
        print(f"Options: {scenario['options']}")
    except Exception as e:
        print(f"Error getting scenario: {e}")
        return
    
    # Test 2: Submit a decision
    print("\nTest 2: Submitting decision (selecting first option)...")
    try:
        data = json.dumps({"decision": 0}).encode('utf-8')
        req = urllib.request.Request(
            f"{base_url}/api/evaluate",
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        print("Success! Got response:")
        print(f"Consequences: {result['consequences']}")
        if result.get('next_scenario'):
            print("\nNext scenario:")
            print(f"ID: {result['next_scenario']['id']}")
            print(f"Description: {result['next_scenario']['description']}")
            print(f"State: {result['next_scenario']['state']}")
    except Exception as e:
        print(f"Error submitting decision: {e}")


if __name__ == "__main__":
    test_api()
