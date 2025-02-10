WHITE = -1
BLACK = 1


class Othello:
    def __init__(self):
        self.size = 8
        self.board = []

        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(0)
            self.board.append(row)

        self.initialize_board()

    def initialize_board(self):
        mid = self.size // 2
        self.board[mid - 1][mid - 1] = BLACK  # Black piece (○)
        self.board[mid][mid] = BLACK  # Black piece (○)
        self.board[mid - 1][mid] = WHITE  # White piece (●)
        self.board[mid][mid - 1] = WHITE  # White piece (●)

    def display_board(self):
        print("  a b c d e f g h")

        # Print each row with row numbers
        for i in range(self.size):
            row_string = str(i + 1) + " "  # Row number
            for j in range(self.size):
                if self.board[i][j] == BLACK:
                    row_string += "○ "  # Black piece
                elif self.board[i][j] == WHITE:
                    row_string += "● "  # White piece
                else:
                    row_string += ". "  # Empty space
            print(row_string)

    def is_valid_move(self, row, col, player):
        """Check if placing a piece at (row, col) is a valid move for the player."""

        if self.board[row][col] != 0:
            return False

        opponent = -player
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
        move_valid = False  # Flag to check if at least one direction is valid

        for dr, dc in directions:
            r, c = row + dr, col + dc
            captured = []  # List of pieces that would be captured

            # Move in the given direction while opponent pieces are found
            while (
                0 <= r < self.size
                and 0 <= c < self.size
                and self.board[r][c] == opponent
            ):
                r += dr
                c += dc
                captured.append((r, c))  # Keep track of all captured pieces

            # Ensure at least one opponent piece was found and the line ends in a player piece
            if (
                captured
                and 0 <= r < self.size
                and 0 <= c < self.size
                and self.board[r][c] == player
            ):
                move_valid = True  # At least one valid capture direction

        return move_valid

    def get_valid_moves(self, player):
        """Finds and returns all valid moves for the player."""
        valid_moves = []

        # Check every position on the board
        for row in range(self.size):
            for col in range(self.size):
                if self.is_valid_move(row, col, player):
                    valid_moves.append((row, col))  # Add valid move to list

        return valid_moves

    def make_move(self, row, col, player):
        if not self.is_valid_move(row, col, player):
            return False  # Invalid move

        self.board[row][col] = player
        opponent = -player
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

        flipped_pieces = []  # Track flipped pieces for undoing moves

        for dr, dc in directions:
            r, c = row + dr, col + dc
            captured = []

            while (
                0 <= r < self.size
                and 0 <= c < self.size
                and self.board[r][c] == opponent
            ):
                captured.append((r, c))
                r += dr
                c += dc

            if (
                captured
                and 0 <= r < self.size
                and 0 <= c < self.size
                and self.board[r][c] == player
            ):
                for r, c in captured:
                    self.board[r][c] = player  # Flip pieces
                    flipped_pieces.append((r, c))

        return flipped_pieces  # Return flipped pieces to allow undoing moves

    def undo_move(self, row, col, player, flipped_pieces):
        self.board[row][col] = 0  # Remove the piece that was placed
        for r, c in flipped_pieces:
            self.board[r][
                c
            ] = -player  # Flip the captured pieces back to opponent's color

    def evaluate_board(self, player):
        """Simple evaluation function: counts the number of pieces for the player."""
        return sum(row.count(player) for row in self.board)

    def max_value(self, depth):
        if depth == 0:
            return self.evaluate_board(1), None

        best_score = float("-inf")
        best_move = None

        for move in self.get_valid_moves(1):
            row, col = move
            flipped_pieces = self.make_move(row, col, 1)
            score, _ = self.min_value(depth - 1)
            self.undo_move(row, col, 1, flipped_pieces)

            if score > best_score:
                best_score = score
                best_move = move

        return best_score, best_move

    def min_value(self, depth):
        if depth == 0:
            return self.evaluate_board(-1), None

        best_score = float("inf")
        best_move = None

        for move in self.get_valid_moves(-1):
            row, col = move
            flipped_pieces = self.make_move(row, col, -1)
            score, _ = self.max_value(depth - 1)
            self.undo_move(row, col, -1, flipped_pieces)

            if score < best_score:
                best_score = score
                best_move = move

        return best_score, best_move

    def minimax_decision(self, player, depth):
        if player == 1:
            return self.max_value(depth)
        else:
            return self.min_value(depth)

    def declare_winner(self):
        """Determines the winner by counting pieces."""
        black_count = sum(row.count(1) for row in self.board)
        white_count = sum(row.count(-1) for row in self.board)

        print(f"Final Score - Black (○): {black_count}, White (●): {white_count}")

        if black_count > white_count:
            print("🏆 Black (○) Wins!")
        elif white_count > black_count:
            print("🏆 White (●) Wins!")
        else:
            print("🤝 It's a Tie!")

    def game_loop(self):
        """Main loop for turn-based play with player color selection."""

        # Ask the player to choose Black (○) or White (●)
        while True:
            player_choice = (
                input("Do you want to play as Black (○) or White (●)? (B/W): ")
                .strip()
                .lower()
            )
            if player_choice == "b":
                human_player = 1  # Black (○)
                break
            elif player_choice == "w":
                human_player = -1  # White (●)
                break
            else:
                print("Invalid choice! Please enter 'B' for Black or 'W' for White.")

        player = 1  # Black (○) always starts

        while True:
            self.display_board()  # Show the board

            valid_moves = self.get_valid_moves(player)

            # Check if the current player has any valid moves
            if not valid_moves:
                print(
                    f"No valid moves for {'Black (○)' if player == 1 else 'White (●)'}! Passing turn."
                )
                player = -player  # Switch turn

                # Check if BOTH players have no moves (game over)
                if not self.get_valid_moves(player):
                    print("No moves for both players. Game Over!")
                    self.display_board()
                    self.declare_winner()
                    break
                continue  # Skip to next player

            # Determine if it's the human player's turn
            if player == human_player:
                print(f"Your turn ({'Black (○)' if player == 1 else 'White (●)'})!")

                # Display valid moves in 1-based indexing
                print("Valid moves:", [(r + 1, c + 1) for r, c in valid_moves])

                while True:
                    try:
                        move_input = input("Enter your move (row col): ")
                        row, col = map(int, move_input.split())
                        row -= 1  # Convert to zero-based index
                        col -= 1

                        if (row, col) in valid_moves:
                            self.make_move(row, col, player)
                            break
                        else:
                            print("Invalid move! Choose a valid move from the list.")
                    except ValueError:
                        print(
                            "Invalid input! Enter row and column as numbers (e.g., '3 4')."
                        )

            else:
                print(f"AI's turn ({'Black (○)' if player == 1 else 'White (●)'})...")
                _, best_move = self.minimax_decision(player, depth=3)

                if best_move:
                    print(
                        f"AI chooses move: {best_move[0]+1}, {best_move[1]+1}"
                    )  # Display in 1-based index
                    self.make_move(best_move[0], best_move[1], player)

            player = -player  # Switch turns


if __name__ == "__main__":
    game = Othello()
    game.game_loop()
