"""
Simple PPO Implementation for Physical AI Learning and Adaptation
This is a basic implementation to demonstrate the structure of training scripts for Chapter 05
"""
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import gymnasium as gym
from torch.distributions import Normal
import matplotlib.pyplot as plt


class ActorCritic(nn.Module):
    """
    Simple Actor-Critic network for continuous action spaces
    """
    def __init__(self, state_dim, action_dim, hidden_dim=256):
        super(ActorCritic, self).__init__()
        
        # Actor network
        self.actor = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, action_dim)
        )
        
        # Critic network
        self.critic = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, 1)
        )
        
        # Learnable log std for action distribution
        self.log_std = nn.Parameter(torch.zeros(action_dim))
    
    def forward(self, state):
        mu = self.actor(state)
        std = torch.exp(self.log_std)
        value = self.critic(state)
        return mu, std, value
    
    def get_action(self, state):
        mu, std, _ = self.forward(state)
        dist = Normal(mu, std)
        action = dist.sample()
        log_prob = dist.log_prob(action).sum(-1, keepdim=True)
        return action, log_prob
    
    def evaluate(self, state, action):
        mu, std, value = self.forward(state)
        dist = Normal(mu, std)
        log_prob = dist.log_prob(action).sum(-1, keepdim=True)
        entropy = dist.entropy().sum(-1, keepdim=True)
        return log_prob, entropy, value


class PPO:
    """
    Proximal Policy Optimization implementation
    """
    def __init__(self, state_dim, action_dim, lr=3e-4, gamma=0.99, eps_clip=0.2, 
                 K_epochs=4, entropy_coef=0.01):
        self.gamma = gamma
        self.eps_clip = eps_clip
        self.K_epochs = K_epochs
        self.entropy_coef = entropy_coef
        
        self.policy = ActorCritic(state_dim, action_dim)
        self.optimizer = optim.Adam(self.policy.parameters(), lr=lr)
        self.policy_old = ActorCritic(state_dim, action_dim)
        self.policy_old.load_state_dict(self.policy.state_dict())
        
        self.MseLoss = nn.MSELoss()
    
    def update(self, states, actions, rewards, logprobs, is_terminals):
        # Monte Carlo estimate of state rewards
        discounted_rewards = []
        running_reward = 0
        
        for reward, is_terminal in zip(reversed(rewards), reversed(is_terminals)):
            if is_terminal:
                running_reward = 0
            running_reward = reward + self.gamma * running_reward
            discounted_rewards.insert(0, running_reward)
        
        # Normalize discounted rewards
        discounted_rewards = torch.tensor(discounted_rewards, dtype=torch.float32)
        discounted_rewards = (discounted_rewards - discounted_rewards.mean()) / (discounted_rewards.std() + 1e-5)
        
        # Convert to tensors
        old_states = torch.stack(states).detach()
        old_actions = torch.stack(actions).detach()
        old_logprobs = torch.stack(logprobs).detach()
        
        # Optimize policy for K epochs
        for _ in range(self.K_epochs):
            # Evaluate old actions and values
            logprobs, entropy, state_values = self.policy_old.evaluate(old_states, old_actions)
            
            # Find the ratio (pi_theta / pi_theta__old)
            ratios = torch.exp(logprobs - old_logprobs.detach())
            
            # Compute advantages
            advantages = discounted_rewards - state_values.detach()
            
            # Compute surrogate losses
            surr1 = ratios * advantages
            surr2 = torch.clamp(ratios, 1 - self.eps_clip, 1 + self.eps_clip) * advantages
            actor_loss = -torch.min(surr1, surr2).mean()
            
            # Compute critic loss
            critic_loss = self.MseLoss(state_values, discounted_rewards.unsqueeze(1))
            
            # Compute total loss
            loss = actor_loss + 0.5 * critic_loss - self.entropy_coef * entropy.mean()
            
            # Take gradient step
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
        
        # Copy new weights into old policy
        self.policy_old.load_state_dict(self.policy.state_dict())


def train_ppo(env_name="Pendulum-v1", n_episodes=1000, max_timesteps=1000):
    """
    Train a PPO agent on a given environment
    """
    # Create environment
    env = gym.make(env_name)
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.shape[0]
    
    # Initialize PPO agent
    ppo = PPO(state_dim, action_dim)
    
    # Training loop
    print(f"Starting PPO training on {env_name}")
    running_reward = 0
    avg_length = 0
    log_interval = 50
    log_rewards = []
    log_episodes = []
    
    for i_episode in range(1, n_episodes+1):
        state, _ = env.reset()
        state = torch.FloatTensor(state)
        episode_reward = 0
        
        for t in range(max_timesteps):
            # Running policy_old
            action, logprob = ppo.policy_old.get_action(state)
            action = action.cpu().data.numpy()
            
            # Perform action
            next_state, reward, done, _, _ = env.step(action)
            next_state = torch.FloatTensor(next_state)
            
            # Save the transition
            ppo.buffer.states.append(state)
            ppo.buffer.actions.append(torch.FloatTensor(action))
            ppo.buffer.logprobs.append(logprob)
            ppo.buffer.rewards.append(reward)
            ppo.buffer.is_terminals.append(done)
            
            state = next_state
            episode_reward += reward
            
            if done:
                break
        
        running_reward += episode_reward
        avg_length += t
        
        # Update PPO agent
        ppo.update()
        
        # Logging
        if i_episode % log_interval == 0:
            avg_reward = running_reward / log_interval
            avg_length = int(avg_length / log_interval)
            log_rewards.append(avg_reward)
            log_episodes.append(i_episode)
            
            print(f'Episode {i_episode}/{n_episodes}, avg. reward: {avg_reward:.2f}, avg length: {avg_length}')
            
            running_reward = 0
            avg_length = 0
    
    # Plot learning curve
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(log_episodes, log_rewards)
    plt.title('PPO Learning Curve')
    plt.xlabel('Episode')
    plt.ylabel('Average Reward')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('static/training-scripts/chapter-05/results/ppo_learning_curve.png', dpi=150)
    plt.show()
    
    return log_rewards, log_episodes


class Memory:
    """
    Memory buffer for storing transitions
    """
    def __init__(self):
        self.states = []
        self.actions = []
        self.logprobs = []
        self.rewards = []
        self.is_terminals = []
    
    def clear_memory(self):
        del self.states[:]
        del self.actions[:]
        del self.logprobs[:]
        del self.rewards[:]
        del self.is_terminals[:]


# Add memory to PPO class
def add_memory_to_ppo():
    PPO.buffer = Memory()


if __name__ == "__main__":
    # Add memory to PPO class
    add_memory_to_ppo()
    
    # Run training
    print("This is a demonstration of PPO training implementation for Chapter 05 of the Physical AI course.")
    print("For a complete run, you would need to install additional dependencies like gymnasium and pybullet.")
    
    # Note: This is a simplified example that demonstrates the structure
    # A full implementation would require more sophisticated handling
    print("\nImplementation structure ready for advanced learning and adaptation experiments.")