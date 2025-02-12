import time
import os

ROW_LETTERS = ['A', 'B', 'C']

class HumanPlayer:
    def __init__(self, shape: str):
        self.shape = shape

    def mark_square(self, board):
        while True:
            self.choice = input("Enter the square to mark ([Row][Col]): ").upper().strip()
            if len(self.choice) != 2:
                print("Invalid Input. Please try again.")
                continue

            row_letter, col_number = self.choice[0], self.choice[1]

            if row_letter not in ROW_LETTERS or not col_number.isdigit() or int(col_number) not in range(1, 4):
                print("Entered square doesn't exist. Please try again.")
                continue

            row = ROW_LETTERS.index(row_letter)  # Convert row letter to index (0,1,2)
            col = int(col_number) - 1  # Convert column number to index (0,1,2)

            if board[row][col] != " ":
                print(f"'{self.choice}' square is already marked. Choose a different square.")
                continue

            # Mark the square with the player's shape
            board[row][col] = self.shape
            break


class AIPlayer:
    def __init__(self, shape: str):
        self.shape = shape  # 'X' or 'O'
        self.opponent_shape = 'O' if shape == 'X' else 'X'  # Opponent's shape

    def mark_square(self, players, board):
        # Prioritize blocking, then winning
        move = self.find_best_move(board)
        
        if move:
            row, col = move
            board[row][col] = self.shape

    def find_best_move(self, board):
        # First, check if the AI needs to block the opponent's winning move
        move = self.find_block_move(board)
        if move:
            return move
        
        # Then, check if the AI can win
        move = self.find_winning_move(board)
        if move:
            return move

        # Otherwise, make a strategic move (center if available, then random)
        return self.find_center_move(board) or self.find_random_move(board)

    def find_block_move(self, board):
        """Find a move to block the opponent from winning."""
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    # Temporarily place the opponent's mark to check for a win
                    board[row][col] = self.opponent_shape
                    if self.check_winner(board) == self.opponent_shape:
                        board[row][col] = " "  # Undo the move
                        return (row, col)
                    board[row][col] = " "  # Undo the move
        return None

    def find_winning_move(self, board):
        """Find a move where the AI can win."""
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    # Temporarily place the AI's mark to check for a win
                    board[row][col] = self.shape
                    if self.check_winner(board) == self.shape:
                        board[row][col] = " "  # Undo the move
                        return (row, col)
                    board[row][col] = " "  # Undo the move
        return None

    def find_center_move(self, board):
        """Return the center if available."""
        if board[1][1] == " ":
            return (1, 1)  # The center is a strong position
        return None

    def find_random_move(self, board):
        """Return a random valid move if no immediate win/block is needed."""
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    return (row, col)
        return None

    def check_winner(self, board):
        """Check if the current player has won."""
        win_patterns = [
            [(0, 0), (0, 1), (0, 2)],  # Row 1
            [(1, 0), (1, 1), (1, 2)],  # Row 2
            [(2, 0), (2, 1), (2, 2)],  # Row 3
            [(0, 0), (1, 0), (2, 0)],  # Column 1
            [(0, 1), (1, 1), (2, 1)],  # Column 2
            [(0, 2), (1, 2), (2, 2)],  # Column 3
            [(0, 0), (1, 1), (2, 2)],  # Diagonal (\)
            [(0, 2), (1, 1), (2, 0)]   # Diagonal (/)
        ]
        
        for pattern in win_patterns:
            a, b, c = pattern
            if board[a[0]][a[1]] == board[b[0]][b[1]] == board[c[0]][c[1]] and board[a[0]][a[1]] != " ":
                return board[a[0]][a[1]]  # Return the symbol ('X' or 'O') of the winner

        return None


def main():
    while True:
        clear_screen()
        logo()
        print("*** Main Menu ***\n")
        print("[1] Singleplayer")
        print("[2] Multiplayer")
        print("[E] Exit")

        choice = input("\nPlease choose an option: ").strip().upper()

        if choice == "1":
            print("Starting Singleplayer game...")
            time.sleep(1)
            singleplayer_game()
            break
        elif choice == "2":
            print("Starting Multiplayer game...")
            time.sleep(1)
            multiplayer_game()
            break
        elif choice == "E":
            print("Exiting the game...")
            time.sleep(1)
            break
        else:
            print("Invalid choice! Please try again.")
            time.sleep(1)


def singleplayer_game():
    board = [[" " for _ in range(3)] for _ in range(3)]

    while True:
        human_player_shape = input("\nChoose a shape (X or O): ").strip().upper()
        if human_player_shape in ['X', 'O']:
            ai_player_shape = 'O' if human_player_shape == 'X' else 'X'
            break
        else:
            print("Invalid choice! Please enter 'X' or 'O'.")
    
    human_player = HumanPlayer(human_player_shape)
    ai_player = AIPlayer(ai_player_shape)
    players = [human_player, ai_player]

    game_over = False
    while not game_over:
        for player in players:
            print(f"\n*** Player ({player.shape}) ***")
            display_board(board)
            print("\n")
            
            if isinstance(player, HumanPlayer):
                player.mark_square(board)
            else:
                player.mark_square(players, board)  # AI takes its turn

            winner_index = check_winner(players, board)
            if winner_index is not None:
                display_board(board)
                if winner_index == players.index(human_player):
                    print("\nYou Won! 🎉")
                elif winner_index == -1:
                    print("\nTie 🤝")
                else:
                    print("\nYou Lost! 😔")
                game_over = True
                break

    sub_menu(game_mode="singleplayer")


def multiplayer_game():
    board = [[" " for _ in range(3)] for _ in range(3)]

    while True:
        player1_shape = input("\nChoose a shape for Player 1 (X or O): ").strip().upper()
        if player1_shape in ['X', 'O']:
            player2_shape = 'O' if player1_shape == 'X' else 'X'
            break
        else:
            print("Invalid choice! Please enter 'X' or 'O'.")
            continue

    player1 = HumanPlayer(player1_shape)
    player2 = HumanPlayer(player2_shape)

    players = [player1, player2]

    display_board(board)

    game_over = False
    while not game_over:
        for index, player in enumerate(players):  # Use enumerate() instead of index lookup
            print(f"\n*** Player {index + 1} ({player.shape}) ***")
            player.mark_square(board)
            display_board(board)
            
            winner_index = check_winner(players, board)
            if winner_index is not None:
                if winner_index in [0, 1]:
                    print(f"\nPlayer {winner_index + 1} Won! 🎉")
                else:
                    print("\nTie 🤝")
                game_over = True
                break

    sub_menu(game_mode="multiplayer")


def check_winner(players, board):
    """Check if there is a winner and return the winner's index."""
    win_patterns = [
        [(0, 0), (0, 1), (0, 2)],  # Row 1
        [(1, 0), (1, 1), (1, 2)],  # Row 2
        [(2, 0), (2, 1), (2, 2)],  # Row 3
        [(0, 0), (1, 0), (2, 0)],  # Column 1
        [(0, 1), (1, 1), (2, 1)],  # Column 2
        [(0, 2), (1, 2), (2, 2)],  # Column 3
        [(0, 0), (1, 1), (2, 2)],  # Diagonal (\)
        [(0, 2), (1, 1), (2, 0)]   # Diagonal (/)
    ]
    
    # Check for winner in all patterns
    for pattern in win_patterns:
        a, b, c = pattern
        if board[a[0]][a[1]] == board[b[0]][b[1]] == board[c[0]][c[1]] and board[a[0]][a[1]] != " ":
            # Return the index of the player who won
            winner_symbol = board[a[0]][a[1]]
            for i, player in enumerate(players):
                if player.shape == winner_symbol:
                    return i  # Index of the winning player
    
    # Check for tie: if the board is full and no winner, it's a tie
    if all(board[r][c] != " " for r in range(3) for c in range(3)):
        return -1  # Tie condition
    
    return None  # No winner yet


def display_board(board):
    """Prints the Tic Tac Toe board"""
    print("\n")
    print("  ", end='')
    for i in range(1, 4):
        print(f" {i} ", end=" ")
    print("\n")
    for row in range(3):
        print(f"{ROW_LETTERS[row]} ", end=" ") 
        print(" | ".join(board[row]))
        if row < 2:
            print("  ", end='')
            print("-" * 11)

# Clear screen for different platforms
def clear_screen():
    if os.name == "nt":  # For Windows
        os.system("cls")
    else:  # For Unix-like (Linux/Mac)
        os.system("clear")

def sub_menu(game_mode):
    while True:
        print("\n[1] Play Again")
        print("[2] Main Menu")
        print("[E] Exit")

        choice = input("\nChoose an option: ").strip().upper()

        if choice == "1":
            print("Starting a new game...")
            time.sleep(1)
            # Call the current game mode again (either singleplayer or multiplayer)
            if game_mode == "singleplayer":
                singleplayer_game()
            elif game_mode == "multiplayer":
                multiplayer_game()
            break  # Exit the loop to restart the game mode
        elif choice == "2":
            print("Returning to the main menu...")
            time.sleep(1)
            main()  # Call the main menu function to return to the main menu
            break  # Exit the loop after going to the main menu
        elif choice == "E":
            print("Exiting the game...")
            time.sleep(1)
            exit()  # Exit the game
        else:
            print("Invalid choice! Please try again.")
            time.sleep(1)

def logo():
    print(
        """                                          ⭕❕⭕❕❌
▀█▀ █ █▀▀   ▀█▀ ▄▀█ █▀▀   ▀█▀ █▀█ █▀▀     ➖➕➖➕➖
 █  █ █▄▄    █  █▀█ █▄▄    █  █▄█ ██▄     ⭕❕⁣❌❕⭕
                                          ➖➕➖➕➖
                                          ❌❕❌❕⭕ 
"""
)

if __name__ == "__main__":
    main()
