# Q-Learning Games Documentation

This repository contains two games, **Proximity** and **Tic-Tac-Toe**, both featuring an AI opponent trained using Q-Learning reinforcement learning.

## Project Structure

```
Q-learning games/
├── proximity/
│   ├── proximity_main.py       # Main entry point and AI logic for Proximity
│   ├── proximity_gui.py        # GUI implementation using Tkinter
│   ├── proximity_train.py      # Training script for the AI
│   └── proximity_brain.pkl     # Saved Q-table (AI memory)
├── tic_tac_toe/
│   ├── tictactoe_main.py       # Main entry point and AI logic for Tic-Tac-Toe
│   ├── tictactoe_gui.py        # GUI implementation using Tkinter
│   ├── tictactoe_train.py      # Training script for the AI
│   └── tictactoe_brain.pkl     # Saved Q-table (AI memory)
```

---

## Proximity

### 1. Main Entry Point (`proximity_main.py`)
This file contains the core AI logic and serves as the entry point to run the game.

- **`ProximityBot` Class**:
    - **`__init__`**: Initializes the bot, loads the Q-table from `proximity_brain.pkl`, and sets learning parameters (`epsilon`, `alpha`, `gamma`).
    - **`load_brain` / `save_brain`**: Handles persistence of the Q-table using `pickle`.
    - **`get_state`**: Converts the board state (ownership map + current tile value) into a string key for the Q-table.
    - **`choose_action`**: Decides the next move using an Epsilon-Greedy strategy (exploration vs. exploitation).
    - **`learn` / `update_q`**: Implements the Q-Learning update rule (Bellman equation) to adjust Q-values based on rewards and future prospects.

- **Execution**:
    - If run directly (`python proximity/proximity_main.py`), it initializes the `ProximityApp` from `proximity_gui.py`.

### 2. GUI (`proximity_gui.py`)
Handles the graphical user interface using `tkinter`.

- **`ProximityApp` Class**:
    - Sets up the 5x5 grid, score labels, and game loop.
    - **`start_new_game`**: Resets the board and shuffles the tile pool (numbers 1-25).
    - **`on_click`**: Handles user input. If valid, executes the move, updates the board, and triggers the AI turn.
    - **`run_ai_turn`**: Calls `bot.choose_action` to get the AI's move, executes it, and calls `bot.learn` to update the AI's strategy based on the outcome.
    - **`execute_move`**: Places a tile and handles the "capture" logic (converting neighbors of lower value).

### 3. Training (`proximity_train.py`)
A headless script to train the AI by playing against itself or a random agent.

- **`train(iterations)`**:
    - Runs a specified number of simulated games.
    - Uses `ProximityBot` to make decisions for both Player 1 and Player 2.
    - Updates the Q-table after every move and assigns a final reward (win/loss) at the end of each game.
    - Saves the improved brain to `proximity_brain.pkl`.

---

## Tic-Tac-Toe

### 1. Main Entry Point (`tictactoe_main.py`)
This file contains the core AI logic and serves as the entry point to run the game.

- **`SmartBot` Class**:
    - **`__init__`**: Initializes the bot and loads the Q-table.
    - **`choose_action`**: Returns a move and a boolean indicating if it was a random move (for exploration).
    - **`learn` / `update_q`**: Updates Q-values based on game states and rewards.
    - **`get_state`**: detailed string representation of the board for Q-table lookups.

- **Execution**:
    - If run directly (`python "tic_tac_toe/tictactoe_main.py"`), it initializes the `TicTacToeApp` from `tictactoe_gui.py`.

### 2. GUI (`tictactoe_gui.py`)
Handles the graphical user interface using `tkinter`.

- **`TicTacToeApp` Class**:
    - Sets up the 3x3 grid.
    - **`on_click`**: Handling human moves.
    - **`run_ai_turn`**: Triggers the AI to move.
    - **`check_game_over`**: Checks for win conditions or draws and displays results.

### 3. Training (`tictactoe_train.py`)
A high-speed training script using "Self-Play".

- **`train(iterations)`**:
    - Simulates thousands of games where the AI plays against itself.
    - Both "players" share the same Q-table (`SmartBot` instance), effectively learning from both winning and losing perspectives simultaneously.
    - Updates q-values immediately after moves and at terminal states (Win/Loss/Draw).

---
