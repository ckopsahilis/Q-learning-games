import random
import os
import time
import pickle

import tkinter as tk

class SmartBot:
    def __init__(self, epsilon=0.2):
        self.filename = "tictactoe_brain.pkl"
        self.epsilon = epsilon 
        self.alpha = 0.3    
        self.gamma = 0.9    
        self.last_move = None
        self.last_state = None
        self.q_table = self.load_brain() # <--- Load brain on startup

    def load_brain(self):
        """Tries to load a saved Q-table from a file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'rb') as f:
                    data = pickle.load(f)
                    print(f"Brain loaded! I remember {len(data)} situations.")
                    return data
            except:
                print("Error loading brain. Starting fresh.")
        return {}

    def save_brain(self):
        """Saves the current Q-table to a file"""
        with open(self.filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def get_state(self, board):
        # Ensure consistent state representation
        return str(board)

    def choose_action(self, board, available_moves):
        self.last_state = self.get_state(board)
        
        # If we have played a lot, reduce randomness (Get serious)
        if len(self.q_table) > 200 and self.epsilon > 0.1:
            self.epsilon = 0.1

        if random.uniform(0, 1) < self.epsilon:
            action = random.choice(available_moves)
            is_random = True
        else:
            is_random = False
            state_actions = self.q_table.get(self.last_state, {})
            valid_scores = {k: v for k, v in state_actions.items() if k in available_moves}
            if valid_scores:
                action = max(valid_scores, key=valid_scores.get)
            else:
                action = random.choice(available_moves)
        
        self.last_move = action
        return action, is_random

    def learn(self, reward, new_board, game_over):
        if self.last_state is None: return

        if self.last_state not in self.q_table:
            self.q_table[self.last_state] = {}
        if self.last_move not in self.q_table[self.last_state]:
            self.q_table[self.last_state][self.last_move] = 0.0

        old_value = self.q_table[self.last_state][self.last_move]
        next_max = 0
        if not game_over:
            next_state = self.get_state(new_board)
            if next_state in self.q_table:
                next_max = max(self.q_table[next_state].values(), default=0)

        new_value = old_value + self.alpha * (reward + (self.gamma * next_max) - old_value)
        self.q_table[self.last_state][self.last_move] = new_value

    def update_q(self, state, action, reward, next_state, game_over):
        """Pure math update, no file saving per move - for training script compatibility"""
        if state not in self.q_table:
            self.q_table[state] = {}
        if action not in self.q_table[state]:
            self.q_table[state][action] = 0.0

        old_value = self.q_table[state][action]
        next_max = 0
        if not game_over:
            # Note: next_state might vary in format depending on caller, but training script passes string
            if next_state in self.q_table:
                next_max = max(self.q_table[next_state].values(), default=0)

        # Bellman Equation
        new_value = old_value + self.alpha * (reward + (self.gamma * next_max) - old_value)
        self.q_table[state][action] = new_value
        
        # Save progress after every game ends
        if game_over:
            self.save_brain()

if __name__ == "__main__":
    from tictactoe_gui import TicTacToeApp
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()