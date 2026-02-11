import tkinter as tk
from tkinter import messagebox
import random
from proximity_main import ProximityBot

# --- The Twisted GUI ---
class ProximityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Twisted Proximity")
        self.root.geometry("600x750")
        self.root.configure(bg="#2c3e50")

        # 5x5 GRID
        self.rows = 5
        self.cols = 5
        self.bot = ProximityBot()
        
        self.board = [] 
        self.tile_pool = []
        self.turn_index = 0
        self.p1_score = 0
        self.p2_score = 0
        self.game_over = False
        
        self.prev_ai_state = None
        self.prev_ai_action = None

        self.create_widgets()
        self.start_new_game()

    def create_widgets(self):
        # Header Frame
        self.top_frame = tk.Frame(self.root, bg="#2c3e50")
        self.top_frame.pack(pady=10)

        # Rules Explanation
        rules_text = (
            "RULES: Place tiles 1-25. Each number appears exactly once.\n"
            "If you place a higher number next to an opponent's tile\n"
            "(Up, Down, Left, Right), you capture it."
        )
        self.lbl_rules = tk.Label(self.top_frame, text=rules_text, font=("Arial", 10), fg="#bdc3c7", bg="#2c3e50", justify="center")
        self.lbl_rules.pack(pady=(0, 10))

        self.lbl_status = tk.Label(self.top_frame, text="Your Turn", font=("Arial", 18, "bold"), fg="white", bg="#2c3e50")
        self.lbl_status.pack()

        self.lbl_next_tile = tk.Label(self.top_frame, text="Tile: ?", font=("Arial", 28, "bold"), fg="#f1c40f", bg="#2c3e50")
        self.lbl_next_tile.pack(pady=5)

        # Board Grid
        self.board_frame = tk.Frame(self.root, bg="#34495e", padx=5, pady=5)
        self.board_frame.pack()
        
        self.buttons = []
        for r in range(self.rows):
            row_btns = []
            for c in range(self.cols):
                btn = tk.Button(self.board_frame, text="", font=("Arial", 16, "bold"), width=4, height=2,
                                command=lambda r=r, c=c: self.on_click(r, c))
                btn.grid(row=r, column=c, padx=3, pady=3)
                row_btns.append(btn)
            self.buttons.append(row_btns)

        # Score Board
        self.score_frame = tk.Frame(self.root, bg="#2c3e50")
        self.score_frame.pack(pady=20)
        
        self.lbl_p1_score = tk.Label(self.score_frame, text="You: 0", font=("Arial", 14, "bold"), fg="#2ecc71", bg="#2c3e50")
        self.lbl_p1_score.pack(side=tk.LEFT, padx=30)
        
        self.lbl_p2_score = tk.Label(self.score_frame, text="AI: 0", font=("Arial", 14, "bold"), fg="#e74c3c", bg="#2c3e50")
        self.lbl_p2_score.pack(side=tk.RIGHT, padx=30)

        self.btn_reset = tk.Button(self.root, text="New Game", command=self.start_new_game, bg="#95a5a6", fg="black")
        self.btn_reset.pack(pady=10)

    def start_new_game(self):
        self.board = [{'val': 0, 'owner': 0} for _ in range(self.rows * self.cols)]
        
        # 1-25 Pool
        self.tile_pool = list(range(1, 26))
        random.shuffle(self.tile_pool)
        
        self.turn_index = 0
        self.game_over = False
        self.prev_ai_state = None
        self.prev_ai_action = None
        
        self.update_ui()
        self.lbl_status.config(text="Your Turn")
        
    def update_ui(self):
        if self.turn_index < len(self.tile_pool):
            current_val = self.tile_pool[self.turn_index]
            self.lbl_next_tile.config(text=f"Current Tile: {current_val}")
        else:
            self.lbl_next_tile.config(text="Game Over")

        p1_total = 0
        p2_total = 0
        
        for r in range(self.rows):
            for c in range(self.cols):
                idx = r * self.cols + c
                cell = self.board[idx]
                btn = self.buttons[r][c]
                
                if cell['val'] > 0:
                    btn.config(text=str(cell['val']), relief="sunken")
                    if cell['owner'] == 1:
                        btn.config(bg="#2ecc71", fg="white")
                        p1_total += cell['val']
                    else:
                        btn.config(bg="#e74c3c", fg="white")
                        p2_total += cell['val']
                else:
                    btn.config(text="", bg="#ecf0f1", relief="raised")
        
        self.lbl_p1_score.config(text=f"You: {p1_total}")
        self.lbl_p2_score.config(text=f"AI: {p2_total}")
        self.p1_score = p1_total
        self.p2_score = p2_total

    def on_click(self, r, c):
        if self.game_over: return
        if self.turn_index % 2 != 0: return # AI Turn

        idx = r * self.cols + c
        if self.board[idx]['owner'] != 0: return

        current_val = self.tile_pool[self.turn_index]
        caps = self.execute_move(idx, current_val, 1)
        
        if self.prev_ai_state:
            available = [i for i, x in enumerate(self.board) if x['owner'] == 0]
            next_tile = self.tile_pool[self.turn_index + 1] if self.turn_index + 1 < len(self.tile_pool) else 0
            reward = -5 if caps > 0 else 0
            state = self.bot.get_state(self.board, next_tile)
            self.bot.learn(self.prev_ai_state, self.prev_ai_action, reward, state, available)

        self.turn_index += 1
        self.update_ui()
        
        if self.turn_index >= len(self.tile_pool):
            self.end_game()
        else:
            self.lbl_status.config(text="AI is thinking...", fg="#e74c3c")
            self.root.after(700, self.run_ai_turn)

    def run_ai_turn(self):
        if self.game_over: return
        
        current_val = self.tile_pool[self.turn_index]
        available = [i for i, x in enumerate(self.board) if x['owner'] == 0]
        
        if not available: return

        move = self.bot.choose_action(self.board, available, current_val)
        caps = self.execute_move(move, current_val, 2)
        
        reward = caps * 10
        current_state = self.bot.get_state(self.board, current_val)
        
        if self.prev_ai_state:
             self.bot.learn(self.prev_ai_state, self.prev_ai_action, 0, current_state, available)
        
        self.prev_ai_state = current_state
        self.prev_ai_action = move
        
        next_tile = self.tile_pool[self.turn_index + 1] if self.turn_index + 1 < len(self.tile_pool) else 0
        available_next = [i for i, x in enumerate(self.board) if x['owner'] == 0]
        next_state = self.bot.get_state(self.board, next_tile)
        self.bot.learn(self.prev_ai_state, self.prev_ai_action, reward, next_state, available_next)

        self.turn_index += 1
        self.update_ui()
        self.lbl_status.config(text="Your Turn", fg="white")
        
        if self.turn_index >= len(self.tile_pool):
            self.end_game()

    def execute_move(self, idx, value, pid):
        self.board[idx]['val'] = value
        self.board[idx]['owner'] = pid
        
        captured = 0
        row = idx // self.cols
        col = idx % self.cols
        
        offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for ro, co in offsets:
            nr, nc = row + ro, col + co
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                nidx = nr * self.cols + nc
                neighbor = self.board[nidx]
                
                if neighbor['owner'] != 0 and neighbor['owner'] != pid:
                    if value > neighbor['val']:
                        neighbor['owner'] = pid
                        captured += 1
        return captured

    def end_game(self):
        self.game_over = True
        self.update_ui()
        
        final_reward = 50 if self.p2_score > self.p1_score else -50
        if self.prev_ai_state:
            self.bot.learn(self.prev_ai_state, self.prev_ai_action, final_reward, None, [])
        self.bot.save_brain()

        if self.p1_score > self.p2_score:
            msg = "You Won! The AI has been defeated."
        elif self.p2_score > self.p1_score:
            msg = "AI Won! Better luck next time."
        else:
            msg = "It's a Draw!"
            
        messagebox.showinfo("Game Over", f"Final Score:\nYou: {self.p1_score}\nAI: {self.p2_score}\n\n{msg}")


