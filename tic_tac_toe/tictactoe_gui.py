import tkinter as tk
from tkinter import messagebox
from tictactoe_main import SmartBot

# --- The GUI Interface ---
class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe AI")
        self.root.geometry("400x500")
        self.root.configure(bg="#2c3e50")

        self.bot = SmartBot()
        self.board = [' '] * 9
        self.human = 'X'
        self.ai = 'O'
        self.player_turn = True # Human starts
        self.game_over = False
        
        self.buttons = []
        self.create_widgets()

    def create_widgets(self):
        # Header Frame
        self.header_frame = tk.Frame(self.root, bg="#2c3e50")
        self.header_frame.pack(pady=20)
        
        self.lbl_status = tk.Label(self.header_frame, text="Your Turn (X)", font=("Arial", 16, "bold"), fg="white", bg="#2c3e50")
        self.lbl_status.pack()

        # Game Board Frame
        self.board_frame = tk.Frame(self.root, bg="#34495e", padx=10, pady=10)
        self.board_frame.pack()

        for i in range(9):
            btn = tk.Button(self.board_frame, text="", font=("Arial", 24, "bold"), width=5, height=2,
                            command=lambda idx=i: self.on_click(idx))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

        # Reset Button
        self.btn_reset = tk.Button(self.root, text="New Game", command=self.reset_game, font=("Arial", 12), bg="#95a5a6", fg="black")
        self.btn_reset.pack(pady=20)

    def on_click(self, idx):
        if self.game_over: return
        if not self.player_turn: return
        if self.board[idx] != ' ': return

        # Human Move
        self.make_move(idx, self.human)
        
        if self.check_game_over(self.human): return

        # AI Turn
        self.player_turn = False
        self.lbl_status.config(text="AI is thinking...", fg="#e74c3c")
        self.root.after(500, self.run_ai_turn)

    def run_ai_turn(self):
        if self.game_over: return

        available = [i for i, x in enumerate(self.board) if x == ' ']
        if not available: return

        # AI Move
        move, is_random = self.bot.choose_action(self.board, available)
        self.make_move(move, self.ai)
        
        if self.check_game_over(self.ai): return
        
        self.player_turn = True
        self.lbl_status.config(text="Your Turn (X)", fg="white")

    def make_move(self, idx, player):
        self.board[idx] = player
        color = "#2ecc71" if player == self.human else "#e74c3c"
        self.buttons[idx].config(text=player, fg=color)

    def check_game_over(self, player):
        wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        won = any(all(self.board[i] == player for i in w) for w in wins)
        
        if won:
            self.game_over = True
            msg = "You Won!" if player == self.human else "AI Won!"
            color = "#2ecc71" if player == self.human else "#e74c3c"
            self.lbl_status.config(text=msg, fg=color)
            
            reward = 1 if player == self.ai else -1
            self.bot.learn(reward, self.board, True)
            self.bot.save_brain()
            
            messagebox.showinfo("Game Over", msg)
            return True

        if ' ' not in self.board:
            self.game_over = True
            self.lbl_status.config(text="It's a Draw!", fg="#f1c40f")
            
            self.bot.learn(0, self.board, True)
            self.bot.save_brain()

            messagebox.showinfo("Game Over", "It's a Draw!")
            return True

        return False

    def reset_game(self):
        self.board = [' '] * 9
        self.game_over = False
        self.player_turn = True
        self.lbl_status.config(text="Your Turn (X)", fg="white")
        for btn in self.buttons:
            btn.config(text="", fg="black", bg="#ecf0f1")


