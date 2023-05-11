import sys
import math

def max_value(state):
    max = -100000000000

    if state == 1:
        return -1

    for move in range(1, 4):
        if state - move > 0:
            m = min_value(state-move)
            max = m if m > max else max

    return max


def min_value(state):
    min = 10000000000000

    if state == 1:
        return 1

    for move in range(1, 4):
        if state - move > 0:
            m = max_value(state-move)
            min = m if m < min else min

    return min


def minimax_decision(state, turn):
    best_move = None
    if turn == 0:  # MAX' turn
        max = -100000000000

        for move in range(1, 4):
            if state - move > 0:
                m = min_value(state - move)
                if m > max:
                    max = m
                    best_move = move

    else:
        min = 10000000000000

        for move in range(1, 4):
            if state - move > 0:
                m = max_value(state-move)
                if m < min:
                    min = m
                    best_move = move

    return best_move


def negamax_decision(state):
    best_move = None
    if (state == 1):
        return -1, 1
   
    max = -100000000000

    for move in range(1, 4):
        if state - move > 0:
            m = negamax_decision(state - move)
            newval = - m[1]
            if newval > max:
                max = newval
                best_move = move

    return best_move, max


def negamax_with_tt(state, depth, alpha, beta, tt):
    
    hash_table = hash(state)
    
    # Check if the current state is already in the transposition table
    if hash_table in tt:
        tt_value = tt[hash_table]
        if tt_value[0] is not None and tt_value[1] is not None:
            return tt_value[0], tt_value[1]
    
    # Check if the maximum search depth has been reached or the game is over
    if depth == 0 or state == 1:
        return -1, 1
    
    best_utility = None
    best_move = None
    
    for move in range(1, 4):
        if state - move > 0:
            # Make a move and recursively search the resulting state
            m = negamax_with_tt(state - move, depth - 1, -beta, -alpha, tt)
            newval = -m[0]
            
            # Update the best move and utility found so far
            if best_utility is None or newval > best_utility:
                best_utility = newval
                best_move = move
            
            # Update alpha and check if a beta cutoff occurred
            alpha = max(alpha, newval)
            if alpha >= beta:
                break
    
    # Update the transposition table with the best utility and move
    tt[hash_table] = (best_utility, best_move)
    
    return best_utility, best_move


def play_nim(state):
    # Initialize the transposition table
    tt = {}
    turn = 0

    while state != 1:
        # Call the modified Negamax function with the transposition table
        value, move = negamax_with_tt(state, 10, -float("inf"), float("inf"), tt)
        print(str(state) + ": " + ("MAX" if not turn else "MIN") + " takes " + str(move) + ' with utility ' + str(value))



        #input()
        state -= move
        turn = 1 - turn

    print("1: " + ("MAX" if not turn else "MIN") + " looses")


def main():
    """
    Main function that will parse input and call the appropriate algorithm. You do not need to understand everything
    here!
    """

    try:
        if len(sys.argv) != 2:
            raise ValueError

        state = int(sys.argv[1])
        if state < 1 or state > 100:
            raise ValueError

        play_nim(state)

    except ValueError:
        print('Usage: python nim.py NUMBER')
        return False


if __name__ == '__main__':
    main()
