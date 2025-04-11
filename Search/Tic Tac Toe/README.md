## Instructions  

Complete "Tictactoe" project [instractions](https://cs50.harvard.edu/ai/2024/projects/0/tictactoe/)  

## Background    

Tic Tac Toe is one of the world's most famous games. Although the rules are simple and the number of moves is small, you still need to think carefully to avoid losing the game.  

Creating a program where the computer is one of the players can be approached in two ways: to apply a template by which the computer chooses a move or to apply ML methods by which the computer finds the best move in relation to the current state.  

### Conditional approach  

There are 3 scripts in "condition_approach" folder, run from the terminal. "tictactoe1.py" choses moves randomly of the possible ones so it's not hard to beat it, "tictactoe2.py" has predefined moves in relation to the current state while "tictactoe3.py" has significantly more predefined moves and is not so easy to beat.

The board of this game has only nine fields, yet the total number of possible states of this game is over 250,000! For games with a larger number of fields (possible combinations), an ML approach is necessary.

## Task  

While "runner.py" script contains all of the code to run the graphical interface for the game, "tictactoe.py" contains all of the logic.   
- All functions except the Minimax function are technical in nature, each of them solves individual questions: who has the next turn on a board, returns the set of all possible actions, returns the winner of the game, if there is one, and so on.  
- Minimax function uses mimimax algorithm to determine the best move for each player. The Minimax algorithm converts a move into a numerical value: for a Max player, it assigns 1 to a winning move, -1 to a losing move, and 0 to a draw. The opposite is true for a Min player. So, Max player is trying to maximize the score and Min player is trying to minimize the score by exploring all possible moves. In short, Max picks the move with the highest minimum score, assuming Min tries to reduce it.  
- Functions max_value and min_value are helper functions that apply alpha-beta pruning to skip unnecessary evaluations and improve efficiency. They stop the search if the Max player has a move with a value of 1 or the Min player has a move with a value of -1.