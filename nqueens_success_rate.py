import sys
import random
import math

MAXQ = 100


def in_conflict(column, row, other_column, other_row):
    """
    Checks if two locations are in conflict with each other.
    :param column: Column of queen 1.
    :param row: Row of queen 1.
    :param other_column: Column of queen 2.
    :param other_row: Row of queen 2.
    :return: True if the queens are in conflict, else False.
    """
    if column == other_column:
        return True  # Same column
    if row == other_row:
        return True  # Same row
    if abs(column - other_column) == abs(row - other_row):
        return True  # Diagonal

    return False


def in_conflict_with_another_queen(row, column, board):
    """
    Checks if the given row and column correspond to a queen that is in conflict with another queen.
    :param row: Row of the queen to be checked.
    :param column: Column of the queen to be checked.
    :param board: Board with all the queens.
    :return: True if the queen is in conflict, else False.
    """
    for other_column, other_row in enumerate(board):
        if in_conflict(column, row, other_column, other_row):
            if row != other_row or column != other_column:
                return True
    return False


def count_conflicts(board):
    """
    Counts the number of queens in conflict with each other.
    :param board: The board with all the queens on it.
    :return: The number of conflicts.
    """
    cnt = 0

    for queen in range(0, len(board)):
        for other_queen in range(queen+1, len(board)):
            if in_conflict(queen, board[queen], other_queen, board[other_queen]):
                cnt += 1

    return cnt


def evaluate_state(board):
    """
    Evaluation function. The maximal number of queens in conflict can be 1 + 2 + 3 + 4 + .. +
    (nquees-1) = (nqueens-1)*nqueens/2. Since we want to do ascending local searches, the evaluation function returns
    (nqueens-1)*nqueens/2 - countConflicts().

    :param board: list/array representation of columns and the row of the queen on that column
    :return: evaluation score
    """
    return (len(board)-1)*len(board)/2 - count_conflicts(board)


def print_board(board):
    """
    Prints the board in a human readable format in the terminal.
    :param board: The board with all the queens.
    """
    print("\n")

    for row in range(len(board)):
        line = ''
        for column in range(len(board)):
            if board[column] == row:
                line += 'Q' if in_conflict_with_another_queen(
                    row, column, board) else 'q'
            else:
                line += '.'
        print(line)


def init_board(nqueens):
    """
    :param nqueens integer for the number of queens on the board
    :returns list/array representation of columns and the row of the queen on that column
    """

    board = []

    for column in range(nqueens):
        board.append(random.randint(0, nqueens-1))

    return board


"""
------------------ Do not change the code above! ------------------
"""


def state_space(board):
    state_space = []

    for column, row in enumerate(board):
        for state in range(len(board)):
            if state == row:
                state_space.append('Q')
            if state != row:
                state_space.append('.')

    return state_space


def heuristic_state_space(board):
    heuristic_state_space = state_space(board)
    best_successor_evaluation = evaluate_state(board)
    set_of_best_successors = []
    i = 0
    for column, row in enumerate(board):
        for possible_successor in range(len(board)):
            # if current queen is not at that state
            if possible_successor != row:
                possible_successor_board = board.copy()
                possible_successor_board[column] = possible_successor
                successor_evaluation = evaluate_state(possible_successor_board)
                heuristic_state_space[i] = successor_evaluation
                if successor_evaluation == best_successor_evaluation:
                    set_of_best_successors.append(i)
                if successor_evaluation > best_successor_evaluation:
                    best_successor_evaluation = successor_evaluation
                    set_of_best_successors.clear()
                    set_of_best_successors.append(i)
            i = i + 1
    best_successor = random.choice(set_of_best_successors)

    move_queen_in_collumn = math.ceil((best_successor + 1) / len(board))
    move_queen_to_position = best_successor - \
        ((move_queen_in_collumn - 1) * len(board))
    board[move_queen_in_collumn - 1] = move_queen_to_position
    return board

def heuristic_state_space_improved(board):
    heuristic_state_space = state_space(board)
    best_successor_evaluation = evaluate_state(board)
    set_of_best_successors = []
    i = 0
    for column, row in enumerate(board):
        for possible_successor in range(len(board)):
            # if current queen is not at that state
            if possible_successor != row:
                possible_successor_board = board.copy()
                possible_successor_board[column] = possible_successor
                successor_evaluation = evaluate_state(possible_successor_board)
                heuristic_state_space[i] = successor_evaluation
                if successor_evaluation == best_successor_evaluation:
                    set_of_best_successors.append(i)
                if successor_evaluation > best_successor_evaluation:
                    best_successor_evaluation = successor_evaluation
                    set_of_best_successors.clear()
                    set_of_best_successors.append(i)
            i = i + 1
    best_successor = random.choice(set_of_best_successors)

    move_queen_in_collumn = math.ceil((best_successor + 1) / len(board))
    move_queen_to_position = best_successor - \
        ((move_queen_in_collumn - 1) * len(board))
    board[move_queen_in_collumn - 1] = move_queen_to_position
    return board


def random_search(board):
    """
    This function is an example and not an efficient solution to the nqueens problem. What it essentially does is flip
    over the board and put all the queens on a random position.
    :param board: list/array representation of columns and the row of the queen on that column
    """

    i = 0
    optimum = (len(board) - 1) * len(board) / 2

    while evaluate_state(board) != optimum:
        i += 1
        print('iteration ' + str(i) + ': evaluation = ' +
              str(evaluate_state(board)))
        if i == 1000:  # Give up after 1000 tries.
            break

        # For each column, place the queen in a random row
        for column, row in enumerate(board):
            board[column] = random.randint(0, len(board)-1)

    if evaluate_state(board) == optimum:
        print('Solved puzzle!')

    print('Final state is:')
    print_board(board)


def hill_climbing_pseudo_code(board):
    """
    Hill-climbing algorithm for the n-queens problem. A heuristic function h(n) computes how 
    many pair's of queens are attacking one another in the current state space. A queen can only 
    move vertically within it's column. For every possible move of a queen the value h is computed 
    for that position in the state space. The successor's are all possible moves generated by moving 
    a queen. Successors = ((number of states - 1) * number of states))/2.
    For every position In the state space the value h is computed for every possible successor. 
    The hill climbing algorithm chooses the best successor among the possible set of successor's. 
    If there is more than one best successor a random successor is chosen among the set of best successor's. 

    a) The initial pseudo code should stop once the evaluation of the current state space is equal to the new state space.
        Thus the algorithm stops once it founds a shoulder.  

    b) The algortihm fails if it encounters a shoulder. 

    c) One improvement to the pseudocode is to search further if the code is at a shoulder. So if the current state evaluation is 
        equal to the evaluation of the new possiblr state evaluation to continue searching instead of stopping there. Because after 
        the shoulder there might be still a local maxima and could find a solution still 
    :param board: list/array representation of columns and the row of the queen on that column
    """

    i = 0
    optimum = (len(board) - 1) * len(board) / 2

    while evaluate_state(board) != optimum:
        i += 1
        #print('iteration ' + str(i) + ': evaluation = ' + str(evaluate_state(board)))
        if i == 1000:  # Give up after 1000 tries.
            break
        board_evaluation = evaluate_state(board)
        board = heuristic_state_space(board)
        successor_board_evaluation = evaluate_state(board)
        if (board_evaluation == successor_board_evaluation):
            break

    if evaluate_state(board) == optimum:
        print('Solved puzzle!')

    #print('Final state is:')
    #print_board(board)


def hill_climbing_improved(board):
    """
    Hill-climbing algorithm for the n-queens problem. A heuristic function h(n) computes how 
    many pair's of queens are attacking one another in the current state space. A queen can only 
    move vertically within it's column. For every possible move of a queen the value h is computed 
    for that position in the state space. The successor's are all possible moves generated by moving 
    a queen. Successors = ((number of states - 1) * number of states))/2.
    For every position In the state space the value h is computed for every possible successor. 
    The hill climbing algorithm chooses the best successor among the possible set of successor's. 
    If there is more than one best successor a random successor is chosen among the set of best successor's. 

    a) The initial pseudo code should stop once the evaluation of the current state space is equal to the new state space.
        Thus the algorithm stops once it founds a shoulder.  

    c) One improvement to the pseudocode is to search further if the code is at a shoulder. So if the current state evaluation is 
        equal to the evaluation of the new possiblr state evaluation to continue searching instead of stopping there. Because after 
        the shoulder there might be still a local maxima and could find a solution still 
    :param board: list/array representation of columns and the row of the queen on that column
    """

    i = 0
    optimum = (len(board) - 1) * len(board) / 2

    while evaluate_state(board) != optimum:
        i += 1
        print('iteration ' + str(i) + ': evaluation = ' +
              str(evaluate_state(board)))
        if i == 1000:  # Give up after 1000 tries.
            break
        board = heuristic_state_space_improved(board)

    if evaluate_state(board) == optimum:
        print('Solved puzzle!')

    #print('Final state is:')
    #print_board(board)


def time_to_temperature(board):
    pass


def simulated_annealing(board):
    """
    Implement this yourself.
    :param board:
    :return:
    """
    
    pass


def main():
    """
    Main function that will parse input and call the appropriate algorithm. You do not need to understand everything
    here!
    """

    try:
        if len(sys.argv) != 2:
            raise ValueError

        n_queens = int(sys.argv[1])
        if n_queens < 1 or n_queens > MAXQ:
            raise ValueError

    except ValueError:
        print('Usage: python n_queens.py NUMBER')
        return False

    i = 0
    while (i != 9):
        print('Which algorithm to use?')
        algorithm = 2 #input('1: random, 2: hill-climbing (pseudo code), 3: hill-climbing (improved), 4: simulated annealing \n')

        try:
            algorithm = int(algorithm)

            if algorithm not in range(1, 5):
                raise ValueError

        except ValueError:
            print('Please input a number in the given range!')
            return False

        board = init_board(n_queens)
        #print('Initial board: \n')
        #print_board(board)

        if algorithm == 1:
            random_search(board)
        if algorithm == 2:
            hill_climbing_pseudo_code(board)
        if algorithm == 3:
            hill_climbing_improved(board)
        if algorithm == 4:
            simulated_annealing(board)
        
        i = i + 1 


# This line is the starting point of the program.
if __name__ == "__main__":
    main()