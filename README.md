# Q-Learning Games

This repository contains two classic games: **Tic-Tac-Toe** and **Proximity**, each featuring an AI opponent trained using Q-Learning (Reinforcement Learning).

## Games

### 1. Proximity
A strategic board game where you claim tiles by placing higher numbers adjacent to opponent tiles. The goal is to own the most tiles by the end of the game.

- **Main Script**: `proximity/proximity_main.py`
- **Training Script**: `proximity/proximity_train.py`

### 2. Tic-Tac-Toe
The classic game of X's and O's. The AI is trained to play perfectly (or near-perfectly) against human opponents.

- **Main Script**: `tic_tac_toe/tictactoe_main.py`
- **Training Script**: `tic_tac_toe/tictactoe_train.py`

## Documentation

For a detailed explanation of the code architecture and AI logic, please refer to [CODE_DOCUMENTATION.md](CODE_DOCUMENTATION.md).

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd Q-learning-games
   ```

2. Ensure you have Python installed. The only dependency is `tkinter` (which is included with standard Python installations).

## Usage

### Playing the Games

Run the main scripts to launch the graphical interface:

```bash
# Play Proximity
python proximity/proximity_main.py

# Play Tic-Tac-Toe
# Note: Directory name is "tic_tac_toe"
python "tic_tac_toe/tictactoe_main.py"
```

### Training the AI

You can retrain the AI bots by running the training scripts. This will update the `.pkl` brain files.

```bash
# Train Proximity
python proximity/proximity_train.py

# Train Tic-Tac-Toe
python "tic_tac_toe/tictactoe_train.py"
```

## Structure

- `*_main.py`: The entry point for the game. Contains the AI logic (`Bot` class) and launches the GUI.
- `*_gui.py`: Handles the `tkinter` user interface.
- `*_train.py`: Headless script for training the AI via self-play or simulation.
- `*.pkl`: Serialized Q-table containing the AI's learned knowledge with 50000 practice games.

## Requirements

- Python 3.x
- `tkinter` (usually included with Python)
- No external libraries required (uses standard `random`, `pickle`, `os`, `time`, `math`).

## License

[MIT License](LICENSE)