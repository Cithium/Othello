import time

WHITE = -1
BLACK = 1
DEPTH = 6


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
        print("  1 2 3 4 5 6 7 8")

        for i in range(self.size):
            row_string = str(i + 1) + " "
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
        move_valid = False

        for dr, dc in directions:
            r, c = row + dr, col + dc
            captured = []

            while (
                0 <= r < self.size
                and 0 <= c < self.size
                and self.board[r][c] == opponent
            ):
                r += dr
                c += dc
                captured.append((r, c))

            if (
                captured
                and 0 <= r < self.size
                and 0 <= c < self.size
                and self.board[r][c] == player
            ):
                move_valid = True

        return move_valid

    def get_valid_moves(self, player):
        """Finds and returns all valid moves for the player."""
        valid_moves = []

        for row in range(self.size):
            for col in range(self.size):
                if self.is_valid_move(row, col, player):
                    valid_moves.append((row, col))

        return valid_moves

    def make_move(self, row, col, player):
        if not self.is_valid_move(row, col, player):
            return False

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

        flipped_pieces = []

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
        self.board[row][col] = 0
        for r, c in flipped_pieces:
            self.board[r][
                c
            ] = -player  # Flip the captured pieces back to opponent's color

    def evaluate_board1(self, player):
        """Simple evaluation function: counts the number of pieces for the player."""
        return sum(row.count(player) for row in self.board)

    def evaluate_board(self, player):
        """Improved evaluation function with positional weights."""
        corner_weight = 10  # High value for corners
        edge_weight = 5  # Moderate value for edges
        piece_weight = 1  # Default piece count value

        score = 0
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == player:
                    if (r, c) in [(0, 0), (0, 7), (7, 0), (7, 7)]:  # Corners
                        score += corner_weight
                    elif (r == 0 or r == 7) or (c == 0 or c == 7):  # Edges
                        score += edge_weight
                    else:
                        score += piece_weight
        return score

    def max_value(self, depth, alpha, beta, start_time, time_limit):
        if depth == 0 or time.time() - start_time >= time_limit:
            return self.evaluate_board(BLACK), None

        best_score = float("-inf")
        best_move = None

        for move in self.get_valid_moves(BLACK):
            row, col = move
            flipped_pieces = self.make_move(row, col, BLACK)
            score, _ = self.min_value(depth - 1, alpha, beta, start_time, time_limit)
            self.undo_move(row, col, BLACK, flipped_pieces)

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, best_score)
            if alpha >= beta:
                break

        return best_score, best_move

    def min_value(self, depth, alpha, beta, start_time, time_limit):
        if depth == 0 or time.time() - start_time >= time_limit:
            return self.evaluate_board(WHITE), None

        best_score = float("inf")
        best_move = None

        for move in self.get_valid_moves(WHITE):
            row, col = move
            flipped_pieces = self.make_move(row, col, WHITE)
            score, _ = self.max_value(depth - 1, alpha, beta, start_time, time_limit)
            self.undo_move(row, col, WHITE, flipped_pieces)

            if score < best_score:
                best_score = score
                best_move = move

            beta = min(beta, best_score)
            if beta <= alpha:
                break

        return best_score, best_move

    def minimax_decision(self, player, depth, time_limit=5):
        start_time = time.time()
        if player == 1:
            return self.max_value(
                depth, float("-inf"), float("inf"), start_time, time_limit
            )
        else:
            return self.min_value(
                depth, float("-inf"), float("inf"), start_time, time_limit
            )

    def declare_winner(self):
        black_count = sum(row.count(BLACK) for row in self.board)
        white_count = sum(row.count(WHITE) for row in self.board)

        print(f"Final Score - Black (○): {black_count}, White (●): {white_count}")

        if black_count > white_count:
            print("🏆 Black (○) Wins!")
        elif white_count > black_count:
            print("🏆 White (●) Wins!")
        else:
            print("🤝 It's a Tie!")

    def game_loop(self):
        """Main loop for turn-based play with player color selection."""

        while True:
            player_choice = (
                input("Do you want to play as Black (○) or White (●)? (B/W): ")
                .strip()
                .lower()
            )
            if player_choice == "b":
                human_player = BLACK  # Black (○)
                break
            elif player_choice == "w":
                human_player = WHITE  # White (●)
                break
            else:
                print("Invalid choice! Please enter 'B' for Black or 'W' for White.")

        player = 1

        while True:
            self.display_board()

            valid_moves = self.get_valid_moves(player)

            if not valid_moves:
                print(
                    f"❌ No valid moves for {'Black (○)' if player == BLACK else 'White (●)'}! Passing turn."
                )
                player = -player

                if not self.get_valid_moves(player):
                    print("⚠️ No moves for both players. Game Over!")
                    self.display_board()
                    self.declare_winner()
                    break
                continue  # Skip to next player

            if player == human_player:
                print(f"Your turn ({'Black (○)' if player == BLACK else 'White (●)'})!")

                print("Valid moves:", [(r + 1, c + 1) for r, c in valid_moves])

                while True:
                    try:
                        move_input = input("Enter your move in the format ROW COL : ")
                        row, col = map(int, move_input.split())
                        row -= 1
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
            # **AI Turn**
            else:
                print(
                    f"AI's turn ({'Black (○)' if player == BLACK else 'White (●)'})..."
                )
                _, best_move = self.minimax_decision(player, DEPTH)

                # Display in human readble index
                if best_move:
                    print(f"AI chooses move: {best_move[0]+1}, {best_move[1]+1}")
                    self.make_move(best_move[0], best_move[1], player)

            player = -player


if __name__ == "__main__":
    game = Othello()
    game.game_loop()
