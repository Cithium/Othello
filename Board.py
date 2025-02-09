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
        self.board[mid-1][mid-1] = 1  # Black piece (○)
        self.board[mid][mid] = 1      # Black piece (○)
        self.board[mid-1][mid] = -1     # White piece (●)
        self.board[mid][mid-1] = -1     # White piece (●)

    def display_board(self):
        print("  a b c d e f g h") 

        # Print each row with row numbers
        for i in range(self.size):
            row_string = str(i+1) + " "  # Row number
            for j in range(self.size):
                if self.board[i][j] == 1:
                    row_string += "○ "  # Black piece
                elif self.board[i][j] == -1:
                    row_string += "● "  # White piece
                else:
                    row_string += ". "  # Empty space
            print(row_string)

    def is_valid_move(self, row, col, player):
        """Check if placing a piece at (row, col) is a valid move for the player."""
        
        if self.board[row][col] != 0:
            return False 
        

        opponent = -player
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        move_valid = False  # Flag to check if at least one direction is valid

    
        for dr, dc in directions:
            r, c = row + dr, col + dc
            captured = []  # List of pieces that would be captured
            
            # Move in the given direction while opponent pieces are found
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == opponent:
                r += dr
                c += dc
                captured.append((r, c))  # Keep track of all captured pieces
            
            # Ensure at least one opponent piece was found and the line ends in a player piece
            if captured and 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == player:
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
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        flipped_pieces = []  # Track flipped pieces for undoing moves
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            captured = []
            
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == opponent:
                captured.append((r, c))
                r += dr
                c += dc
            
            if captured and 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == player:
                for r, c in captured:
                    self.board[r][c] = player  # Flip pieces
                    flipped_pieces.append((r, c))
        
        return flipped_pieces  # Return flipped pieces to allow undoing moves
    
    def undo_move(self, row, col, player, flipped_pieces):
        self.board[row][col] = 0  # Remove the piece that was placed
        for r, c in flipped_pieces:
            self.board[r][c] = -player  # Flip the captured pieces back to opponent's color

    
    def evaluate_board(self, player):
        """Simple evaluation function: counts the number of pieces for the player."""
        return sum(row.count(player) for row in self.board)
    
    def max_value(self, depth):
        if depth == 0:
            return self.evaluate_board(1), None
        
        best_score = float('-inf')
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
        
        best_score = float('inf')
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



if __name__ == "__main__":
    game = Othello()
    game.display_board()
    
    #black_moves = game.get_valid_moves(1)
    #print("Valid moves for Black (○):", black_moves)
    
    #white_moves = game.get_valid_moves(-1)
   # print("Valid moves for White (●):", white_moves)
    
    #row, col = black_moves[0]
       # print(f"Applying move for Black at ({row+1}, {col+1})")
       # game.make_move(row, col, 1)
        #game.make_move(4, 5, -1)
        #game.make_move(5, 2, 1)
        #game.make_move(1, 4, -1 )

        # Test Minimax with split functions
    _, best_move = game.minimax_decision(1, 3)
    print("Best move for Black (○):", best_move)

    _, best_move = game.minimax_decision(-1, 3)
    print("Best move for White (●):", best_move)


    
