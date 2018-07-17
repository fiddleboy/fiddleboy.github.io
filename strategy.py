"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from typing import Any, Union
from stack import Stack, Tree

# TODO: Adjust the type annotation as needed.


def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def rough_outcome_strategy(game: Any) -> Any:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2 # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move


# TODO: Implement a recursive version of the minimax strategy.


def reminimax(game: Any) -> Any:
    """
    Return the best move for current state.
    """
    current = game.current_state
    moves = game.current_state.get_possible_moves()
    empty = []
    for i in moves:
        state = current
        score = -1*get_score(game, state.make_move(i))
        empty.append([score, i])
    return max(empty)[1]


def get_score(game: Any, state: Any) -> int:
    """
    Return the score for the current state player.
    """
    if state.get_possible_moves() == []:
        return result(game, state)
    return max([-1 * get_score(game, state.make_move(x))
                for x in state.get_possible_moves()])


def result(game: Any, state: Any) -> int:
    """
    Return the score for the current position of the current player.
    """
    game.current_state = state
    name = state.get_current_player_name()
    if game.is_winner(name):
        return 1
    elif game.is_winner('p1') or game.is_winner('p2'):
        return -1
    return 0


# TODO: Implement an iterative version of the minimax strategy.


def itminimax(game: Any) -> Any:
    """
    Return a best move based the current state.
    """
    current = game.current_state
    my_stack = Stack()
    initial = Tree(current)
    my_stack.add(initial)
    empty = []
    while not my_stack.is_empty():
        a = my_stack.remove()
        game.current_state = a.state
        if game.is_over(a.state):
            if game.is_winner(a.state.get_current_player_name()):
                a.score = 1
                game.current_state = current
            elif game.is_winner('p1') or game.is_winner('p2'):
                a.score = -1
                game.current_state = current
            else:
                a.score = 0
                game.current_state = current
        elif a.children == []:
            creat_new_items(my_stack, a)
            game.current_state = current
        else:
            a.score = max([-1 * x.score for x in a.children])
            game.current_state = current
        empty.append(a)
    return get_move(empty[0])


def get_index(atree: Tree) -> Union[None, int]:
    """
    Get atree's children index as needed. Otherwise, return None.
    """
    for x in atree.children:
        if x.score * -1 == atree.score:
            return atree.children.index(x)
    return None


def get_move(atree: Tree) -> Any:
    """
    Return the correct move cause the current state.
    """
    index = get_index(atree)
    moves = atree.state.get_possible_moves()
    return moves[index]


def creat_new_items(my_stack: Stack, a: Tree) -> None:
    """
    Add new items into my_stack based on the current situation of a.
    """
    empty = []
    for i in a.state.get_possible_moves():
        childrens = Tree(a.state.make_move(i))
        a.children.append(childrens)
        empty.append(childrens)
    my_stack.add(a)
    if empty != []:
        for x in empty:
            my_stack.add(x)


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
