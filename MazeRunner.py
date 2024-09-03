import random
import sys
from pyamaze import maze, agent, COLOR
from GameSearch import GameSearch


def create_maze(size):
    """
        Creates a maze of the given size.

        Args:
        size (int): Size of the maze (10 or 20).

        Returns:
        maze: A maze object.
        """
    if size == 10:
        my_maze = maze(10, 10)
    elif size == 20:
        my_maze = maze(20, 30)
    else:
        raise ValueError("Invalid maze size")

    my_maze.CreateMaze(loopPercent=100)
    return my_maze


def place_agents(my_maze):
    """
       Places two agents and a goal randomly in the maze.

       Args:
       my_maze (maze): The maze object.

       Returns:
       tuple: Two agent objects and the goal position (row, col).
       """
    while True:
        rand_row1, rand_col1 = random.randint(1, my_maze.rows), random.randint(1, my_maze.cols)
        rand_row2, rand_col2 = (random.randint(1, my_maze.rows),
                                random.randint(1, my_maze.cols))
        goal_row, goal_col = random.randint(1, my_maze.rows), random.randint(1, my_maze.cols)
        if (rand_row1, rand_col1) != (goal_row, goal_col) and (rand_row2, rand_col2) != (goal_row, goal_col):
            break
    max_agent = agent(my_maze, rand_row1, rand_col1, shape='arrow', footprints=True)
    min_agent = agent(my_maze, rand_row2, rand_col2, color=COLOR.red, footprints=True)
    return max_agent, min_agent, (goal_row, goal_col)


def get_human_move(player, search):
    """
    Gets the move input from a human player.

    Args:
    player (tuple): The current position of the human player (row, col).
    search (GameSearch): The search object.

    Returns:
    tuple: The next move (row, col).
    """
    while True:
        try:
            row = int(input("Enter the row: "))
            col = int(input("Enter the column: "))
            if 1 <= row <= search.maze.rows and 1 <= col <= search.maze.cols:
                if (row, col) in search.get_possible_moves((player[0], player[1])):
                    print("get_human_move ", row, " ", col)
                    return (row, col)
                else:
                    print("Invalid move. Try again.")
            else:
                print(f"Invalid input. Enter values between 1 and {search.maze.rows} for row and between 1 "
                      f"and {search.maze.cols} for column")
        except ValueError:
            print("Invalid input")


def minimax_strategy(player, opponent, search):
    """
    Determines the next move using the Minimax strategy.

    Args:
    player (tuple): The current position of the player (row, col).
    opponent (tuple): The current position of the opponent (row, col).
    search (GameSearch): The search object.

    Returns:
    tuple: The best move (row, col).
    """
    return search.find_best_move(player, opponent, 'MM')


def alpha_beta_strategy(player, opponent, search):
    """
     Determines the next move using the Alpha-Beta pruning strategy.

     Args:
     player (tuple): The current position of the player (row, col).
     opponent (tuple): The current position of the opponent (row, col).
     search (GameSearch): The search object.

     Returns:
     tuple: The best move (row, col).
     """
    return search.find_best_move(player, opponent, 'AB')


def visualize_path(my_maze, agent, move):
    """
     Visualizes the path taken by an agent.

     Args:
     my_maze (maze): The maze object.
     agent (agent): The agent object.
     move (tuple): The move to visualize (row, col).
     """
    if move:
        path = [move]
        print(f"Path: {path}")
        my_maze.tracePath({agent: path}, delay=100)
        my_maze.markCells.append((move[0], move[1], COLOR.cyan))


def move_agent(agent, next_move: tuple):
    """
    Moves the agent to the next position.

    Args:
    agent (agent): The agent object.
    next_move (tuple): The next move (row, col).

    Returns:
    tuple: The new position of the agent (row, col).
    """
    return next_move


def main():
    """
    Main function to run the MazeRunner game.
    """
    if len(sys.argv) != 4:
        print("Usage: MazeRunner.py [Player] [searchmethod] [size]")
        return

    player_number = int(sys.argv[1])
    search_method = sys.argv[2]
    size = int(sys.argv[3])

    my_maze = create_maze(size)
    max_agent, min_agent, goal_agent = place_agents(my_maze)

    search = GameSearch(my_maze, goal_agent)

    if search_method == 'MM':
        move_strategy = minimax_strategy
    elif search_method == 'AB':
        move_strategy = alpha_beta_strategy
    else:
        raise ValueError("Invalid search method")

    node_count = 0
    depth_level = search.MAX_DEPTH

    my_maze.run()
    while True:
        if player_number == 1:
            # AI is MAX
            ai_move = move_strategy(max_agent.position, min_agent.position, search)
            max_agent = move_agent(max_agent, ai_move)
            visualize_path(my_maze, max_agent, [ai_move])
            node_count += 1

            if search.is_terminal(max_agent.position, min_agent.position):
                print("AI (MAX) wins!")
                break

            print(f"MAX moved: {max_agent.position}")
            print(f"It is MIN's turn: ")
            human_move = get_human_move(min_agent.position, search)
            min_agent = move_agent(min_agent, human_move)
            print("Human moved")
            visualize_path(my_maze, min_agent, human_move)

            if search.is_terminal(max_agent.position, min_agent.position):
                print("Human (MIN) wins!")
                break
        else:
            # AI is MIN
            ai_move = move_strategy(min_agent.position, max_agent.position, search)
            min_agent = move_agent(min_agent, ai_move)
            print("AI move: " + ai_move)
            visualize_path(my_maze, min_agent, ai_move)
            node_count += 1

            if search.is_terminal(max_agent.position, min_agent):
                print("AI (MIN) wins!")
                break

            print(f"MAX moved: {max_agent.position}")
            print(f"It is MIN's turn: ")
            human_move = get_human_move(max_agent.position, search)
            max_agent = move_agent(max_agent, human_move)
            visualize_path(my_maze, max_agent, human_move)

            if search.is_terminal(max_agent.position, min_agent):
                print("Human (MAX) wins!")
                break

    # Write README.txt
    with open("README.txt", "w") as file:
        file.write("Evaluation function: opponent_distance - player_distance\n")
        file.write(f"Number of nodes expanded: {node_count}\n")
        file.write(f"Depth level for look-ahead: {depth_level}\n")


if __name__ == "__main__":
    main()
