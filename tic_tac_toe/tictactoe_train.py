import pickle
import random
import os
import sys

# --- The Brain (Exact copy of the Game logic, but faster) ---
from tictactoe_main import SmartBot

# --- The Headless Game Engine ---
def train(iterations=10000):
    print(f"Initializing High-Speed Training ({iterations} games)...")
    
    # We create two bots, but they will share the SAME Q-table (The Hive Mind)
    # This is 'Self-Play', the most efficient way to train.
    bot = SmartBot(epsilon=0.3) 
    
    wins = 0
    losses = 0
    draws = 0

    for i in range(iterations):
        board = [' ' for _ in range(9)]
        available = list(range(9))
        
        # Tracking history for learning
        p1_moves = [] # (state, action)
        p2_moves = [] # (state, action)
        
        turn = 'P1' 
        game_over = False
        
        while not game_over:
            current_state_str = str(board)
            
            # --- Move Logic ---
            action, _ = bot.choose_action(board, available)
            
            board[action] = 'X' if turn == 'P1' else 'O'
            available.remove(action)
            
            # Record move
            if turn == 'P1': p1_moves.append((current_state_str, action))
            else: p2_moves.append((current_state_str, action))

            # --- Check Win/Draw ---
            # Simplified winner check for speed
            w_cond = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
            has_won = any(all(board[k] == ('X' if turn == 'P1' else 'O') for k in w) for w in w_cond)
            
            if has_won:
                if turn == 'P1':
                    wins += 1
                    # P1 gets +1, P2 gets -1
                    bot.update_q(p1_moves[-1][0], p1_moves[-1][1], 1, None, True)
                    if p2_moves: # P2 lost on previous turn
                         bot.update_q(p2_moves[-1][0], p2_moves[-1][1], -1, None, True)
                else:
                    losses += 1
                    # P2 gets +1, P1 gets -1
                    bot.update_q(p2_moves[-1][0], p2_moves[-1][1], 1, None, True)
                    if p1_moves:
                        bot.update_q(p1_moves[-1][0], p1_moves[-1][1], -1, None, True)
                game_over = True

            elif not available:
                draws += 1
                # Neutral reward for draw
                if p1_moves: bot.update_q(p1_moves[-1][0], p1_moves[-1][1], 0, None, True)
                if p2_moves: bot.update_q(p2_moves[-1][0], p2_moves[-1][1], 0, None, True)
                game_over = True
            
            # --- If game continues, update Q-value for previous move based on current state ---
            if not game_over:
                if turn == 'P1': # P1 just moved, update P2's previous move
                     if p2_moves:
                        bot.update_q(p2_moves[-1][0], p2_moves[-1][1], 0, str(board), False)
                else: # P2 just moved, update P1's previous move
                     if p1_moves:
                        bot.update_q(p1_moves[-1][0], p1_moves[-1][1], 0, str(board), False)

            # Switch turn
            turn = 'P2' if turn == 'P1' else 'P1'

        # Progress Bar
        if iterations >= 10 and i % (iterations // 10) == 0:
            print(f"Progress: {i}/{iterations} games played...")

    # Save at the very end
    bot.save_brain()
    print("\nTraining Complete!")
    print(f"Results -> P1 Wins: {wins}, P2 Wins: {losses}, Draws: {draws}")
    print(f"Total Brain States: {len(bot.q_table)}")
    print("You can now run the main game script!")

if __name__ == "__main__":
    try:
        count = int(input("How many practice games? (Recommend ~50000): "))
    except:
        count = 50000
    train(count)