#!/usr/bin/env python3
"""
Simple test to check the enhanced DQN system
"""

print("🔥 Starting Enhanced DQN Test...")

try:
    import numpy as np
    print("✅ NumPy imported")
    
    import torch
    print("✅ PyTorch imported")
    
    from enhanced_dqn_system import EnhancedFireResponseEnvironment
    print("✅ Enhanced environment imported")
    
    from enhanced_dqn_system import EnhancedDQNAgent
    print("✅ Enhanced agent imported")
    
    # Create environment
    env = EnhancedFireResponseEnvironment()
    print(f"✅ Environment created with {env.state_dim} states, {env.action_dim} actions")
    print(f"📚 Training scenarios loaded: {len(env.scenarios)}")
    
    # Create agent
    agent = EnhancedDQNAgent(
        state_dim=env.state_dim,
        action_dim=env.action_dim
    )
    print("✅ Agent created successfully")
    
    # Test reset
    state, source_id = env.reset()
    print(f"✅ Environment reset: state shape {state.shape}, source_id {source_id}")
    
    # Test action selection
    action = agent.select_action(state, source_id)
    print(f"✅ Action selected: {action}")
    
    # Test step
    next_state, reward, done, info = env.step(action, source_id)
    print(f"✅ Step completed: reward {reward}, done {done}")
    
    print("\n🎯 All tests passed! Enhanced DQN system is working.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
