import pickle
import random
import os
import time

from proximity_main import ProximityBot

def train(iterations):
    rows = 5
    cols = 5
    bot = ProximityBot(epsilon=0.6)
    
    # Clear the brain to ensure it learns the new 5x5 rules from scratch
    bot.q_table = {} 

    print(f"Starting training for {iterations} games on 5x5 Board...")
    start_time = time.time()
    
    for i in range(iterations):
        board = [{'val': 0, 'owner': 0} for _ in range(rows * cols)]
        
        # 1-25 POOL
        pool = list(range(1, 26))
        random.shuffle(pool)
        
        turn = 0
        p1_moves = []
        p2_moves = []
        
        while True:
            available = [idx for idx, c in enumerate(board) if c['owner'] == 0]
            if not available: break
            
            curr_tile = pool[turn]
            is_p1 = (turn % 2 == 0)
            pid = 1 if is_p1 else 2
            move = bot.choose_action(board, available, curr_tile)
            
            board[move]['val'] = curr_tile
            board[move]['owner'] = pid
            
            captured = 0
            r, c = move // cols, move % cols
            
            offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            
            for ro, co in offsets:
                nr, nc = r + ro, c + co
                if 0 <= nr < rows and 0 <= nc < cols:
                    nidx = nr * cols + nc
                    neighbor = board[nidx]
                    if neighbor['owner'] != 0 and neighbor['owner'] != pid:
                        if curr_tile > neighbor['val']:
                            neighbor['owner'] = pid
                            captured += 1

            current_state = bot.get_state(board, curr_tile)
            reward = captured * 10
            
            if is_p1:
                if p1_moves:
                    prev_s, prev_a = p1_moves[-1]
                    bot.update_q(prev_s, prev_a, reward, current_state, available)
                p1_moves.append((current_state, move))
            else:
                if p2_moves:
                    prev_s, prev_a = p2_moves[-1]
                    bot.update_q(prev_s, prev_a, reward, current_state, available)
                p2_moves.append((current_state, move))
            turn += 1
            if turn >= len(pool): break

        s1 = sum(c['val'] for c in board if c['owner'] == 1)
        s2 = sum(c['val'] for c in board if c['owner'] == 2)
        final_reward = 50 if s1 > s2 else -50
        
        if p1_moves: bot.update_q(p1_moves[-1][0], p1_moves[-1][1], final_reward, None, [])
        if p2_moves: bot.update_q(p2_moves[-1][0], p2_moves[-1][1], -final_reward, None, [])

        if i > 0 and i % 5000 == 0:
            print(f"Game {i}/{iterations} | Learned States: {len(bot.q_table)}")

    bot.save_brain()
    print(f"Training Complete in {time.time() - start_time:.2f}s!")

if __name__ == "__main__":
    try:
        count = int(input("How many practice games? (Recommend ~50000): "))
    except:
        count = 50000
    train(count)