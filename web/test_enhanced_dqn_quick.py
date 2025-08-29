#!/usr/bin/env python3
"""
Quick test script for Enhanced DQN system
"""
import sys
import traceback

def test_imports():
    """Test if all modules can be imported"""
    print("🔥 Testing Enhanced DQN System Imports...")
    
    try:
        import torch
        print("✅ PyTorch imported successfully")
        print(f"   Version: {torch.__version__}")
        print(f"   CUDA available: {torch.cuda.is_available()}")
    except ImportError as e:
        print(f"❌ PyTorch import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy imported successfully")
        print(f"   Version: {np.__version__}")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    try:
        from enhanced_dqn_system import EnhancedFireResponseDQN
        print("✅ EnhancedFireResponseDQN imported successfully")
    except ImportError as e:
        print(f"❌ EnhancedFireResponseDQN import failed: {e}")
        return False
    
    try:
        from enhanced_dqn_system import EnhancedDQNAgent
        print("✅ EnhancedDQNAgent imported successfully")
    except ImportError as e:
        print(f"❌ EnhancedDQNAgent import failed: {e}")
        return False
    
    try:
        from enhanced_dqn_system import EnhancedFireResponseEnvironment
        print("✅ EnhancedFireResponseEnvironment imported successfully")
    except ImportError as e:
        print(f"❌ EnhancedFireResponseEnvironment import failed: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality of the enhanced DQN system"""
    print("\n🧪 Testing Basic Functionality...")
    
    try:
        from enhanced_dqn_system import (
            EnhancedFireResponseEnvironment,
            EnhancedDQNAgent
        )
        
        # Create environment
        env = EnhancedFireResponseEnvironment()
        print(f"✅ Environment created: {env.state_dim} states, {env.action_dim} actions")
        
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
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("=" * 50)
    print("Enhanced DQN System Diagnostic Test")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Cannot proceed.")
        return False
    
    # Test basic functionality
    if not test_basic_functionality():
        print("\n❌ Basic functionality tests failed.")
        return False
    
    print("\n🎯 All tests passed! Enhanced DQN system is ready.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
