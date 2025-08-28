#!/usr/bin/env python3
"""
Enhanced DQN Training Script
Trains DQN agent using comprehensive fire response scenarios
"""

import sys
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
    print("⚠️  Enhanced DQN system not available, using basic training")
    sys.exit(1)


def train_enhanced_dqn(num_episodes: int = 1000, save_interval: int = 200):
    """Train enhanced DQN agent with comprehensive scenarios"""

    print("🔥 Enhanced Fire Response DQN Training")
    print("=" * 60)

    # Initialize environment and agent
    env = EnhancedFireResponseEnvironment()
    agent = EnhancedDQNAgent(
        state_dim=env.state_dim,
        action_dim=env.action_dim,
        lr=2e-4,  # Lower learning rate for stability
        gamma=0.99,
        epsilon=1.0,
        epsilon_decay=0.997,
        epsilon_min=0.05
    )
    
    print(f"📊 Environment: {env.state_dim} states, {env.action_dim} actions")
    print(f"🎯 Training scenarios: {len(env.scenarios)}")
    print(f"📚 Training sources: {list(env.source_map.keys())}")
    print(f"🔄 Training episodes: {num_episodes}")
    print()
    
    # Training metrics
    episode_rewards = []
    episode_losses = []
    source_performance = {source: [] for source in env.source_map.keys()}
    
    # Training loop
    for episode in range(num_episodes):
        # Reset environment
        state, source_id = env.reset()
        episode_reward = 0
        episode_loss = 0
        steps = 0
        
        # Get source name for tracking
        source_names = list(env.source_map.keys())
        current_source = (
            source_names[source_id]
            if source_id < len(source_names)
            else "unknown"
        )

        while steps < 100:  # Max steps per episode
            # Select action
            action = agent.select_action(state, source_id)

            # Take step
            next_state, reward, done, info = env.step(action, source_id)
            next_source_id = source_id  # Source stays same within episode

            # Store experience
            agent.store_experience(
                state, action, reward, next_state, done,
                source_id, next_source_id
            )
            
            # Train agent
            loss = agent.train()
            if loss is not None:
                episode_loss += loss
            
            # Update state
            state = next_state
            episode_reward += reward
            steps += 1
            
            if done:
                break
        
        # Update target network periodically
        if episode % 10 == 0:
            agent.update_target_network()
        
        # Track metrics
        episode_rewards.append(episode_reward)
        if episode_loss > 0:
            episode_losses.append(episode_loss / steps)
        
        # Track source-specific performance
        source_performance[current_source].append(episode_reward)
        
        # Progress reporting
        if episode % 50 == 0:
            avg_reward = (
                np.mean(episode_rewards[-50:])
                if episode_rewards else 0
            )
            avg_loss = (
                np.mean(episode_losses[-50:])
                if episode_losses else 0
            )

            print(f"Episode {episode:4d} | "
                  f"Avg Reward: {avg_reward:6.2f} | "
                  f"Avg Loss: {avg_loss:8.4f} | "
                  f"Epsilon: {agent.epsilon:.3f} | "
                  f"Source: {current_source}")

        # Save model periodically
        if episode > 0 and episode % save_interval == 0:
            model_dir = current_dir / "models"
            model_dir.mkdir(exist_ok=True)
            agent.save_model(str(model_dir / f"enhanced_dqn_ep_{episode}.pth"))

    # Final model save
    model_dir = current_dir / "models"
    model_dir.mkdir(exist_ok=True)
    agent.save_model(str(model_dir / "enhanced_dqn_final.pth"))

    # Training summary
    print("\n" + "=" * 60)
    print("🎯 ENHANCED DQN TRAINING COMPLETE!")
    print(f"📊 Total episodes: {num_episodes}")
    print(f"🏆 Final average reward: {np.mean(episode_rewards[-100:]):.2f}")
    print(f"📉 Final epsilon: {agent.epsilon:.3f}")

    # Source-specific performance summary
    print("\n📚 PERFORMANCE BY TRAINING SOURCE:")
    for source, rewards in source_performance.items():
        if rewards:
            avg_reward = np.mean(rewards)
            print(f"   {source:12}: {avg_reward:6.2f} avg reward "
                  f"({len(rewards)} episodes)")

    return agent, episode_rewards, episode_losses


def test_enhanced_dqn():
    """Test the enhanced DQN with different scenario types"""
    
    print("\n🧪 Testing Enhanced DQN Performance")
    print("=" * 40)
    
    # Load or create agent
    env = EnhancedFireResponseEnvironment()
    agent = EnhancedDQNAgent(
        state_dim=env.state_dim,
        action_dim=env.action_dim
    )
    
    # Try to load trained model
    model_path = Path(__file__).parent / "models" / "enhanced_dqn_final.pth"
    if model_path.exists():
        agent.load_model(str(model_path))
        agent.epsilon = 0.0  # Disable exploration for testing
        print("✅ Loaded trained model")
    else:
        print("⚠️  No trained model found, using random agent")
    
    # Test scenarios by category
    categories = set(
        scenario.get("category", "unknown")
        for scenario in env.scenarios
    )

    for category in categories:
        print(f"\n🎭 Testing {category} scenarios:")

        category_rewards = []
        for _ in range(10):  # 10 test runs per category
            # Find scenario of this category
            category_scenarios = [
                s for s in env.scenarios
                if s.get("category") == category
            ]
            if not category_scenarios:
                continue

            # Set specific scenario - use random.choice for list
            import random
            env.current_scenario = random.choice(category_scenarios)
            state, source_id = env.reset()

            total_reward = 0
            for _ in range(20):  # Max 20 steps
                action = agent.select_action(state, source_id)
                state, reward, done, info = env.step(action, source_id)
                total_reward += reward
                if done:
                    break

            category_rewards.append(total_reward)

        if category_rewards:
            avg_reward = np.mean(category_rewards)
            print(f"   Average reward: {avg_reward:.2f}")

    return agent


def main():
    """Main training and testing function"""

    # Training
    agent, rewards, losses = train_enhanced_dqn(num_episodes=500)

    # Testing
    test_enhanced_dqn()

    print("\n✅ Enhanced DQN training and testing complete!")
    print("🎯 Models saved in ./models/ directory")
    print("📊 Ready for integration with web training system")


if __name__ == "__main__":
    main()
