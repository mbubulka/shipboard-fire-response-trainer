"""
Test script for DCA scenarios
"""
from dca_scenario_states import DCAAssessmentManager

def test_scenario_progression():
    """Test the progression through scenarios"""
    manager = DCAAssessmentManager()
    
    # Get initial scenario
    scenario = manager.get_current_scenario()
    if not scenario:
        print("Error: No initial scenario available")
        return
        
    print("\nInitial scenario:")
    print(f"ID: {scenario.scenario_id}")
    print(f"Description: {scenario.description}")
    print(f"Fire class: {scenario.fire_state.class_}")
    print(f"Phase: {scenario.fire_state.phase}")
    print(f"Options: {scenario.options}")
    
    # Submit a decision and check progression
    print("\nSubmitting decision...")
    consequences = manager.submit_decision(0)  # Select first option
    print(f"Consequences: {consequences}")
    
    # Get next scenario
    next_scenario = manager.get_current_scenario()
    if not next_scenario:
        print("Error: No next scenario available")
        return
        
    print("\nNext scenario:")
    print(f"ID: {next_scenario.scenario_id}")
    print(f"Description: {next_scenario.description}")
    print(f"Fire class: {next_scenario.fire_state.class_}")
    print(f"Phase: {next_scenario.fire_state.phase}")
    print(f"Options: {next_scenario.options}")


if __name__ == "__main__":
    test_scenario_progression()
