import random

# ==============================================================================
# Q-LEARNING AGENT (Reinforcement Learning)
# ==============================================================================
class QLearningAgent:
    """
    A Tabular Q-Learning Agent.
    It learns to navigate the environment by mapping discrete States to Actions
    and updating its knowledge using the Bellman Equation based on Rewards.
    """
    
    def __init__(self, actions):
        # The actions the agent can take (e.g., [0..7] for 8-way directional movement)
        self.actions = actions

        # The Q-Table: A dictionary mapping 'States' (Radar tuples) to a list of 'Q-Values' (Confidence scores)
        # Using a dictionary allows us to dynamically map only the states the agent actually visits (Lazy Initialization)
        self.q_table = {}

        # --- HYPERPARAMETERS (The dials we turn to tune the AI's brain) ---
        
        # Alpha (Learning Rate): Determines how much new information overrides old information.
        # 0.1 means it learns gradually. 1.0 would mean it instantly forgets the past.
        self.alpha = 0.1    
        
        # Gamma (Discount Factor): Determines the importance of future rewards.
        # 0.9 makes the agent value long-term survival rather than just the immediate next step.
        self.gamma = 0.9    

        # --- EXPLORATION VS EXPLOITATION (Epsilon-Greedy Strategy) ---
        
        # Epsilon: The probability that the agent will take a random action instead of the best-known one.
        self.epsilon = 1.0          # Starts at 1.0 (100% exploration/randomness) to discover the map
        self.epsilon_decay = 0.995  # The multiplier used to slowly reduce Epsilon after every learning step
        self.epsilon_min = 0.01     # The floor limit: The agent will always explore at least 1% of the time

    def get_q_values(self, state):
        """ 
        Retrieves the Q-Values for a given state. 
        If the state has never been seen before, it dynamically initializes it with 0.0 for all actions.
        """
        if state not in self.q_table:
            self.q_table[state] = [0.0 for _ in self.actions]
        return self.q_table[state]
    
    def choose_action(self, state):
        """ 
        Epsilon-Greedy Policy: Decides whether to take a random exploratory action 
        or exploit the best-known action based on current Q-Table data.
        """
        # 1. EXPLORE: Roll a dice. If it falls under Epsilon, take a completely random step.
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        
        # 2. EXPLOIT: Use the Q-Table to pick the action with the highest confidence value.
        else:
            q_values = self.get_q_values(state)
            max_q = max(q_values)

            # If multiple actions tie for the highest value (e.g., all are 0.0), pick one randomly among them
            best_actions = [i for i, q in enumerate(q_values) if q == max_q]
            return random.choice(best_actions)
        
    def learn(self, state, action_idx, reward, next_state):
        """ 
        The Bellman Equation Implementation.
        Updates the Q-Table based on the reward received and the estimated optimal future value.
        """
        # Fetch current knowledge
        q_values = self.get_q_values(state)
        next_q_values = self.get_q_values(next_state)

        old_q_value = q_values[action_idx]
        next_max_q = max(next_q_values)

        # THE BELLMAN EQUATION:
        # New Q(s,a) = Old Q(s,a) + Alpha * [Reward + Gamma * MaxQ(s',a') - Old Q(s,a)]
        new_q_value = old_q_value + self.alpha * (reward + self.gamma * next_max_q - old_q_value)

        # Update the table with the new calculated knowledge
        self.q_table[state][action_idx] = new_q_value

        # Epsilon Decay: As the agent learns more about the world, it becomes slightly less random
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay