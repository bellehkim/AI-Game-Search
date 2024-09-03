class GameSearch:
    """
    GameSearch class provides the search algorithms for solving the maze game.
    It provides methods for Minimax and Alpha-Beta pruning strategies.
    """
    def __init__(self, maze, goal_position):
        """
        Initializes the GameSearch object.

        Args:
        maze (maze): The maze object.
        goal_position (tuple): The goal position (row, col) in the maze.
        """
        self.maze = maze
        self.goal_position = goal_position
        self.MAX_DEPTH = 5

    def minimax(self, player, opponent, depth, is_max_turn):
        """
        Minimax algorithm to find the best move.

        Args:
        player (tuple): The current position of the player (row, col).
        opponent (tuple): The current position of the opponent (row, col).
        depth (int): The current depth in the search tree.
        is_max_turn (bool): Flag to indicate if it's the maximizing player's turn.

        Returns:
        int: The evaluation value of the move.
        """
        if depth == self.MAX_DEPTH or self.is_terminal(player, opponent):
            return self.utility_function(player, opponent)

        if is_max_turn:
            max_eval = float('-inf')
            for move in self.get_possible_moves(player):
                player = move
                eval = self.minimax(player, opponent, depth + 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_possible_moves(player):
                opponent = move
                eval = self.minimax(player, opponent, depth + 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def alpha_beta_pruning(self, player, opponent, depth, alpha, beta, is_max_turn):
        """
        Alpha-Beta pruning algorithm to find the best move.

        Args:
        player (tuple): The current position of the player (row, col).
        opponent (tuple): The current position of the opponent (row, col).
        depth (int): The current depth in the search tree.
        alpha (float): Alpha value for pruning.
        beta (float): Beta value for pruning.
        is_max_turn (bool): Flag to indicate if it's the maximizing player's turn.

        Returns:
        int: The evaluation value of the move.
        """
        if depth == self.MAX_DEPTH or self.is_terminal(player, opponent):
            return self.utility_function(player, opponent)

        if is_max_turn:
            max_eval = float('-inf')
            for move in self.get_possible_moves(player):
                player = move
                eval = float(self.alpha_beta_pruning(player, opponent, depth + 1, alpha, beta, False))
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
                return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_possible_moves(player):
                opponent = move
                eval = self.alpha_beta_pruning(player, opponent, depth + 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def find_best_move(self, player, opponent, algorithm):
        """
        Finds the best move for the player using the specified algorithm.

        Args:
        player (tuple): The current position of the player (row, col).
        opponent (tuple): The current position of the opponent (row, col).
        algorithm (str): The search algorithm to use ('MM' for Minimax, 'AB' for Alpha-Beta).

        Returns:
        tuple: The best move (row, col).
        """
        best_val = float('-inf')
        best_move = None

        for move in self.get_possible_moves(player):
            if algorithm == 'MM':
                move_val = self.minimax(player, opponent, 0, False)
            elif algorithm == 'AB':
                move_val = self.alpha_beta_pruning(player, opponent, 0, float('-inf'), float('inf'), False)
            else:
                raise ValueError("Unknown algorithm")

            if move_val > best_val:
                best_val = move_val
                best_move = move
        return best_move

    def utility_function(self, player_position, opponent_position):
        """
        Utility function to evaluate the game state.

        Args:
        player_position (tuple): The current position of the player (row, col).
        opponent_position (tuple): The current position of the opponent (row, col).

        Returns:
        int: The evaluation value of the game state.
        """
        goal_position = self.goal_position
        if player_position == goal_position:
            return 1
        elif opponent_position == goal_position:
            return -1
        else:
            return 0

    def is_terminal(self, player, opponent):
        """
        Checks if the game has reached a terminal state.

        Args:
        player (tuple): The current position of the player (row, col).
        opponent (tuple): The current position of the opponent (row, col).

        Returns:
        bool: True if the game is terminal, False otherwise.
        """
        goal_position = self.goal_position
        return player == goal_position or opponent == goal_position

    def get_possible_moves(self, positions):
        """
        Gets the possible moves from the current position.

        Args:
        positions (tuple): The current position (row, col).

        Returns:
        list: A list of possible moves (row, col).
        """
        curr_row, curr_col = positions
        direction_map = {
            'E': (0, 1),
            'W': (0, -1),
            'N': (-1, 0),
            'S': (1, 0)
        }
        result = []

        possible_directions = dict(self.maze.maze_map.get((curr_row, curr_col)))
        for direction, isOpen in possible_directions.items():
            if isOpen == 1:
                row_to_add, col_to_add = direction_map.get(direction)
                new_row = curr_row + row_to_add
                new_col = curr_col + col_to_add
                if 1 <= new_row <= self.maze.rows and 1 <= new_col <= self.maze.cols:
                    result.append((new_row, new_col))
        return result

