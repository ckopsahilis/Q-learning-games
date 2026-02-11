import random
import os
import pickle
import tkinter as tk

# --- The Brain Logic ---
class ProximityBot:
    def __init__(self, filename="proximity_brain.pkl", epsilon=0.0, alpha=0.3, gamma=0.9):
        self.filename = filename
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.q_table = self.load_brain()

    def load_brain(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'rb') as f:
                    return pickle.load(f)
            except:
                return {}
        return {}

    def save_brain(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def get_state(self, board, current_tile_val):
        ownership_map = tuple(c['owner'] for c in board)
        return str((ownership_map, current_tile_val))

    def choose_action(self, board, available_moves, current_tile_val):
        state = self.get_state(board, current_tile_val)
        if state in self.q_table:
            valid_actions = {a: self.q_table[state][a] for a in available_moves if a in self.q_table[state]}
            if valid_actions:
                return max(valid_actions, key=valid_actions.get)
        return random.choice(available_moves)

    def learn(self, prev_state, prev_action, reward, new_state, new_moves):
        if prev_state not in self.q_table: self.q_table[prev_state] = {}
        if prev_action not in self.q_table[prev_state]: self.q_table[prev_state][prev_action] = 0.0

        old_val = self.q_table[prev_state][prev_action]
        next_max = 0
        if new_moves and new_state in self.q_table:
            possible_next = {a: self.q_table[new_state][a] for a in new_moves if a in self.q_table[new_state]}
            if possible_next:
                next_max = max(possible_next.values())

        new_val = old_val + self.alpha * (reward + (self.gamma * next_max) - old_val)
        self.q_table[prev_state][prev_action] = new_val

    # Alias for training script compatibility
    def update_q(self, state, action, reward, next_state, next_moves):
        self.learn(state, action, reward, next_state, next_moves)

if __name__ == "__main__":
    from proximity_gui import ProximityApp
    root = tk.Tk()
    app = ProximityApp(root)
    root.mainloop()