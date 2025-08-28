#!/usr/bin/env python3
"""
Enhanced DQN Evaluation Script
Evaluates trained DQN agent on different fire response scenarios
"""

import sys
import json
import numpy as np
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

try:
    from enhanced_dqn_system import (
        EnhancedFireResponseEnvironment,
        EnhancedDQNAgent
    )
except ImportError:
    print("❌ Enhanced DQN system not available")
    sys.exit(1)


def evaluate_agent_performance():
    """Evaluate trained agent on comprehensive scenarios"""
    
    print("🎯 Enhanced DQN Agent Evaluation")
    print("=" * 50)
    
    # Initialize environment
    env = EnhancedFireResponseEnvironment()
    agent = EnhancedDQNAgent(
        state_dim=env.state_dim,
        action_dim=env.action_dim
    )
    
    # Try to load trained model
    model_path = current_dir / "models" / "enhanced_dqn_final.pth"
    if model_path.exists():
        agent.load_model(str(model_path))
        agent.epsilon = 0.0  # Disable exploration for evaluation
        print("✅ Loaded trained model")
    else:
        print("⚠️  No trained model found, using random agent")
    
    # Evaluation metrics
    results = {
        'total_scenarios': len(env.scenarios),
        'source_performance': {},
        'category_performance': {},
        'scenario_details': []
    }
    
    print(f"📊 Evaluating {len(env.scenarios)} scenarios...")
    
    # Test all scenarios
    for i, scenario in enumerate(env.scenarios):
        env.current_scenario = scenario
        state, source_id = env.reset()
        
        scenario_name = scenario.get('title', f'Scenario {i+1}')
        source_name = scenario.get('source', 'unknown')
        category = scenario.get('category', 'unknown')
        
        total_reward = 0
        actions_taken = []
        
        # Run episode
        for step in range(50):  # Max 50 steps per scenario
            action = agent.select_action(state, source_id)
            actions_taken.append(action)
            
            next_state, reward, done, info = env.step(action, source_id)
            total_reward += reward
            state = next_state
            
            if done:
                break
        
        # Record results
        scenario_result = {
            'title': scenario_name,
            'source': source_name,
            'category': category,
            'reward': total_reward,
            'steps': len(actions_taken),
            'actions': actions_taken[:10]  # First 10 actions only
        }
        results['scenario_details'].append(scenario_result)
        
        # Update source performance
        if source_name not in results['source_performance']:
            results['source_performance'][source_name] = []
        results['source_performance'][source_name].append(total_reward)
        
        # Update category performance
        if category not in results['category_performance']:
            results['category_performance'][category] = []
        results['category_performance'][category].append(total_reward)
        
        # Progress indicator
        if (i + 1) % 10 == 0:
            print(f"   Evaluated {i+1}/{len(env.scenarios)} scenarios...")
    
    # Calculate summary statistics
    print("\n📈 EVALUATION RESULTS:")
    print("=" * 30)
    
    # Overall performance
    all_rewards = [r['reward'] for r in results['scenario_details']]
    print(f"Overall Average Reward: {np.mean(all_rewards):.2f}")
    print(f"Overall Std Deviation:  {np.std(all_rewards):.2f}")
    print(f"Best Scenario Reward:   {np.max(all_rewards):.2f}")
    print(f"Worst Scenario Reward:  {np.min(all_rewards):.2f}")
    
    # Source-specific performance
    print("\n📚 Performance by Training Source:")
    for source, rewards in results['source_performance'].items():
        avg_reward = np.mean(rewards)
        std_reward = np.std(rewards)
        print(f"   {source:15}: {avg_reward:6.2f} ± {std_reward:5.2f} "
              f"({len(rewards)} scenarios)")
    
    # Category-specific performance
    print("\n🎭 Performance by Scenario Category:")
    for category, rewards in results['category_performance'].items():
        avg_reward = np.mean(rewards)
        std_reward = np.std(rewards)
        print(f"   {category:15}: {avg_reward:6.2f} ± {std_reward:5.2f} "
              f"({len(rewards)} scenarios)")
    
    # Best performing scenarios
    print("\n🏆 Top 5 Best Performing Scenarios:")
    best_scenarios = sorted(
        results['scenario_details'],
        key=lambda x: x['reward'],
        reverse=True
    )[:5]
    
    for i, scenario in enumerate(best_scenarios, 1):
        print(f"   {i}. {scenario['title'][:40]}... "
              f"(Reward: {scenario['reward']:.2f})")
    
    # Save detailed results
    results_file = current_dir / "evaluation_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: {results_file}")
    
    return results


def quick_demo():
    """Quick demonstration of the agent in action"""
    
    print("\n🎬 Quick Demo: Agent in Action")
    print("=" * 35)
    
    env = EnhancedFireResponseEnvironment()
    agent = EnhancedDQNAgent(
        state_dim=env.state_dim,
        action_dim=env.action_dim
    )
    
    # Load model if available
    model_path = current_dir / "models" / "enhanced_dqn_final.pth"
    if model_path.exists():
        agent.load_model(str(model_path))
        agent.epsilon = 0.0
    
    # Select a random scenario for demo
    import random
    demo_scenario = random.choice(env.scenarios)
    env.current_scenario = demo_scenario
    
    print(f"🎯 Scenario: {demo_scenario.get('title', 'Unknown')}")
    print(f"📚 Source: {demo_scenario.get('source', 'Unknown')}")
    print(f"🎭 Category: {demo_scenario.get('category', 'Unknown')}")
    print(f"📝 Situation: {demo_scenario.get('situation', 'N/A')[:100]}...")
    print()
    
    state, source_id = env.reset()
    total_reward = 0
    
    print("🎮 Agent Actions:")
    for step in range(10):  # Show first 10 actions
        action = agent.select_action(state, source_id)
        next_state, reward, done, info = env.step(action, source_id)
        
        # Simple action description
        action_desc = f"Action {action}"
        
        print(f"   Step {step+1}: {action_desc} "
              f"(Reward: {reward:+.1f})")
        
        total_reward += reward
        state = next_state
        
        if done:
            print(f"   ✅ Scenario completed!")
            break
    
    print(f"\n🏆 Total Reward: {total_reward:.2f}")


def main():
    """Main evaluation function"""
    
    # Full evaluation
    results = evaluate_agent_performance()
    
    # Quick demo
    quick_demo()
    
    print("\n✅ Enhanced DQN evaluation complete!")
    print("📊 Check evaluation_results.json for detailed analysis")


if __name__ == "__main__":
    main()
