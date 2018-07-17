"""
The Stonehenge game. State and Game.
"""
from typing import Any
from game import Game
from game_state import GameState


class StonehengeGame(Game):
    """
     A game to be played with two players.

     Attribute:
     is_p1_turn: whether is p1's turn
    """
    is_p1_turn: bool

    def __init__(self, is_p1_turn: bool) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.

        No examples available, since this method rely on user input.
        """
        self.current_state = StonehengeState()
        self.current_state.length = \
            int(input('Enter the side length of the board: '))
        self.is_p1_turn = is_p1_turn
        if self.is_p1_turn is True:
            self.current_state.player = 'p1'
        else:
            self.current_state.player = 'p2'
        self.current_state.possible_move = \
            self.current_state.get_initial_moves()
        self.current_state.stonehenge = stone_generator(self.
                                                        current_state.length)

    def get_instructions(self) -> str:
        """
        Return the instructions for this Game.
        """
        instructions = "Players take turns  claiming cells. "
        instructions += 'Who takes at least half of the cells in a line '
        instructions += 'captures that ley-line. '
        instructions += 'Who takes at least half of the ley-lines is winner.'

        return instructions

    def is_over(self, state: 'StonehengeState') -> bool:
        """
        Return whether or not this game is over at state.
        """
        return state.over is True

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.
        """
        if self.current_state.over is True:
            return self.current_state.player != player
        return False

    def str_to_move(self, string: str) -> str:
        """
        Return the move that string represents. If string is not a move,
        return some invalid move.
        """
        if not string.isalpha():
            return 'Invalid Move'
        elif not string.isupper():
            return 'Invalid Move'
        return string


class StonehengeState(GameState):
    """
    A game to be played with two players

    Attribute:
    over: whether the game is over or not
    player: the name of the current player
    length : the length of stonehenge
    possible_move: possible moves
    stonehenge: stonehenge
    p1_claimed: number of ley-lines p1 claimed
    p2_claimed: number of ley-lines p2 claimed
    """
    over: bool
    player: str
    length: int
    possible_move: list
    stonehenge: list
    p1_claimed: int
    p2_claimed: int
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
               'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']

    def __init__(self):
        """
        Initialize this game state and set the current player based on
        is_p1_turn.

        >>> new = StonehengeState()
        >>> new.over
        False
        """
        self.over = False
        self.player = None
        self.possible_move = []
        self.length = None
        self.stonehenge = None
        # ley-lines each player claimed
        self.p1_claimed = 0
        self.p2_claimed = 0

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.
        """
        copy = [x[:] for x in self.stonehenge]
        for items in copy:
            items.append('\n')
        whole_list = sum(copy, [])
        strings = ''
        for items in whole_list:
            strings += items
        return strings

    def get_current_player_name(self) -> str:
        """
        Return 'p1' if the current player is Player 1, and 'p2' if the current
        player is Player 2.

        >>> new = StonehengeState()
        >>> new.player = 'p1'
        >>> new.player
        'p1'
        """
        return self.player

    def get_possible_moves(self) -> list:
        """
        Return all possible moves that can be applied to this state.

        >>> new = StonehengeState()
        >>> new.over = True
        >>> new.get_possible_moves()
        []
        """
        if self.over:
            return []
        return self.possible_move

    def get_initial_moves(self):
        """
        Return a list of initial moves based on length given.
        """
        n = None
        if self.length == 1:
            n = 3
        elif self.length == 2:
            n = 7
        elif self.length == 3:
            n = 12
        elif self.length == 4:
            n = 18
        elif self.length == 5:
            n = 25
        return [StonehengeState.letters[i] for i in range(n)]

    # back up plan
    def make_a_copy(self) -> 'StonehengeState':
        """
        Return a copy of self.

        >>> old = StonehengeState()
        >>> old.stonehenge = []
        >>> new = old.make_a_copy()
        >>> new.stonehenge
        []
        """
        new = StonehengeState()
        new.over = self.over
        new.player = self.player
        new.possible_move = self.possible_move[:]
        new.length = self.length
        new.stonehenge = [x[:] for x in self.stonehenge]
        # ley-lines each player claimed
        new.p1_claimed = self.p1_claimed
        new.p2_claimed = self.p2_claimed
        #new.winner = self.winner
        return new

    def make_move(self, move: str) -> 'StonehengeState':
        """
        Return the GameState that results from applying move to this GameState.
        """
        new_one = self.make_a_copy()
        index_of_row = self.get_row_num(move)
        index_of_column = self.location_in_row(index_of_row, move)
        if self.player == 'p1':
            new_one.stonehenge[index_of_row][index_of_column] = '1'
        else:
            new_one.stonehenge[index_of_row][index_of_column] = '2'
        new_one.possible_move.remove(move)

        # not claimed up means the marker is '@'
        if not self.is_claimed_up(index_of_row, index_of_column):
            # modify new_one without changing self
            new_one.go_claim_up(index_of_row, index_of_column)

        if not self.is_claimed_down(index_of_row, index_of_column):
            new_one.go_claim_down(index_of_row, index_of_column)

        if not self.is_claimed_left(index_of_row, index_of_column):
            new_one.go_claim_left(index_of_row, index_of_column)

        if self.player == 'p1':
            new_one.player = 'p2'
        elif self.player == 'p2':
            new_one.player = 'p1'

        # modify new_one.over if needed
        new_one.check_over()

        return new_one

    def check_over(self) -> None:
        """
        Check and modify game state if the game is over.

        >>> new = StonehengeState()
        >>> new.length = 1
        >>> new.p1_claimed = 3
        >>> new.p2_claimed = 1
        >>> new.check_over()
        >>> new.over
        True
        """
        total = 3*(self.length + 1)
        if self.p1_claimed >= total/2 or self.p2_claimed >= total/2:
            self.over = True
        return None

    def go_claim_up(self, index_of_row: int, index_of_column: int) -> None:
        """
        Modify self, if this ley-line can be claimed up. Otherwise, return None.
        """
        row = index_of_row
        column = index_of_column
        num_of_p1 = 0
        num_of_p2 = 0
        i = 0
        # go right up
        while (0 <= row
               and column < len(self.stonehenge[row])
               and self.stonehenge[row][column] != '@'):
            if self.stonehenge[row][column] == '1':
                num_of_p1 += 1
            elif self.stonehenge[row][column] == '2':
                num_of_p2 += 1
            row -= 2
            column += 2
            i += 1

        row1 = index_of_row + 2
        column1 = index_of_column - 2
        ii = 0
        # go left down
        while (row1 < len(self.stonehenge) - 2
               and column1 > 3
               and (self.stonehenge[row1][column1].isalpha() or
                    self.stonehenge[row1][column1] in ['1', '2'])):
            if self.stonehenge[row1][column1] == '1':
                num_of_p1 += 1
            elif self.stonehenge[row1][column1] == '2':
                num_of_p2 += 1
            row1 += 2
            column1 -= 2
            ii += 1

        # make change to self, if possible
        if num_of_p1 >= (i+ii)/2:
            if self.player == 'p1':
                self.stonehenge[row][column] = '1'
                self.p1_claimed += 1
        elif num_of_p2 >= (i+ii)/2:
            if self.player == 'p2':
                self.stonehenge[row][column] = '2'
                self.p2_claimed += 1

    def go_claim_down(self, index_of_row: int, index_of_column: int) -> None:
        """
        Modify self, if this ley-line can be claimed down.
        Otherwise, return None.
        """
        row = index_of_row
        column = index_of_column
        num_of_p1 = 0
        num_of_p2 = 0
        i = 0
        # go right down
        while (row < len(self.stonehenge)
               and column < len(self.stonehenge[row])
               and self.stonehenge[row][column] != '@'):
            if self.stonehenge[row][column] == '1':
                num_of_p1 += 1
            elif self.stonehenge[row][column] == '2':
                num_of_p2 += 1
            row += 2
            column += 2
            i += 1

        row1 = index_of_row - 1
        column1 = index_of_column - 1
        ii = 0
        while (1 < row1
               and column1 > 3
               and self.stonehenge[row1][column1] != ' '):
            if self.stonehenge[row1][column1] == '1':
                num_of_p1 += 1
            elif self.stonehenge[row1][column1] == '2':
                num_of_p2 += 1
            elif self.stonehenge[row1][column1] == '\\':
                ii += 1
            row1 -= 1
            column1 -= 1

        # make change to self, if possible
        if num_of_p1 >= (i + ii) / 2:
            if self.player == 'p1':
                self.stonehenge[row][column] = '1'
                self.p1_claimed += 1
        elif num_of_p2 >= (i + ii) / 2:
            if self.player == 'p2':
                self.stonehenge[row][column] = '2'
                self.p2_claimed += 1

    def go_claim_left(self, index_of_row: int, index_of_column: int) -> None:
        """
        Modify self, if this ley-line can be claimed down.
        Otherwise, return None.
        """
        row = index_of_row
        column = index_of_column
        num_of_p1 = 0
        num_of_p2 = 0
        i = 0
        # go left
        while (column >= 0
               and self.stonehenge[row][column] != '@'):
            if self.stonehenge[row][column] == '1':
                num_of_p1 += 1
            elif self.stonehenge[row][column] == '2':
                num_of_p2 += 1
            column -= 4
            i += 1

        row1 = index_of_row
        column1 = index_of_column + 4
        ii = 0
        # go right
        if len(self.stonehenge[row1]) == 4 * self.length + 5:
            while (column1 < len(self.stonehenge[row1])
                   and (self.stonehenge[row1][column1].isalpha()
                        or self.stonehenge[row1][column1] in ['1', '2'])):
                if self.stonehenge[row1][column1] == '1':
                    num_of_p1 += 1
                elif self.stonehenge[row1][column1] == '2':
                    num_of_p2 += 1
                column1 += 4
                ii += 1
        else:
            while (column1 < (len(self.stonehenge[row1]) - 4)
                   and (self.stonehenge[row1][column1].isalpha() or
                        self.stonehenge[row1][column1] in ['1', '2'])):
                if self.stonehenge[row1][column1] == '1':
                    num_of_p1 += 1
                elif self.stonehenge[row1][column1] == '2':
                    num_of_p2 += 1
                column1 += 4
                ii += 1

        # make change to self, if possible
        if num_of_p1 >= (i + ii) / 2:
            if self.player == 'p1':
                self.stonehenge[row][column] = '1'
                self.p1_claimed += 1
        elif num_of_p2 >= (i + ii) / 2:
            if self.player == 'p2':
                self.stonehenge[row][column] = '2'
                self.p2_claimed += 1

    def is_claimed_down(self, index_of_row: int, index_of_column: int) -> bool:
        """
        Return if right down ley-line is claimed or not.
        """
        row = index_of_row
        column = index_of_column
        while row < len(self.stonehenge) and column < len(self.stonehenge[row]):
            if self.stonehenge[row][column] == '@':
                return False
            row += 2
            column += 2
        return True

    def is_claimed_left(self, index_of_row: int, index_of_column: int) -> bool:
        """
        Return if right up ley-line is claimed or not.
        """
        row = index_of_row
        column = index_of_column
        while column >= 0:
            if self.stonehenge[row][column] == '@':
                return False
            column -= 4
        return True

    def is_claimed_up(self, index_of_row: int, index_of_column: int) -> bool:
        """
        Return if right up ley-line is claimed or not.
        """
        row = index_of_row
        column = index_of_column
        while row >= 0 and column < len(self.stonehenge[row]):
            if self.stonehenge[row][column] == '@':
                return False
            row -= 2
            column += 2
        return True

    def location_in_row(self, index_of_row: int, move: str) -> int:
        """
        Return the index of the move in a list.
        """
        ax = self.stonehenge[index_of_row]
        return ax.index(move)

    def get_row_num(self, move) -> int:
        """
        Return which row of cells is the move located.

        >>> new = StonehengeState()
        >>> new.get_row_num('A')
        2
        """
        if move in['A', 'B']:
            return 2
            # this is the index of the list, for row, it's the 3rd row
        elif move in ['C', 'D', 'E']:
            return 4
        elif move in ['F', 'G', 'H', 'I']:
            return 6
        elif move in ['J', 'K', 'L', 'M', 'N']:
            return 8
        elif move in ['O', 'P', 'Q', 'R', 'S', 'T']:
            return 10
        elif move in ['U', 'V', 'W', 'X', 'Y']:
            return 12
        return -1

    def is_valid_move(self, move: Any) -> bool:
        """
        Return whether move is a valid move for this GameState.

        >>> new = StonehengeState()
        >>> "A" in new.possible_move
        False
        """
        return move in self.get_possible_moves()

    def __repr__(self) -> str:
        """
        Return a representation of this state (which can be used for
        equality testing).
        """
        copy = self.stonehenge[:]
        for items in copy:
            items.append('\n')
        whole_list = sum(copy, [])
        strings = ''
        for items in whole_list:
            strings += items
        henge = strings

        return 'Player turn: {}\nOver or not: {}\nPossible moves: {}\n'\
               'Ley-line p1 claimed: {}\nLey-line p2 claimed: {}\n'\
               'Size length:\n'.format(self.player, self.over,
                                       self.possible_move, self.p1_claimed,
                                       self.p2_claimed) + henge

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.

        >>> new = StonehengeState()
        >>> new.over = True
        >>> new.rough_outcome()
        -1
        """
        if self.over:
            return -1
        i = []
        ii = []
        iii = []
        for x in self.get_possible_moves():
            a = self.make_move(x)
            if a.over:
                i.append(x)
            else:
                self.helper_rough(a, ii, iii, x)

        if i != []:
            return 1
        elif iii != []:
            return 0
        return -1

    def helper_rough(self, a, ii, iii, x):
        """
        Modify for rought_outcome. A helper.
        """
        ss = []
        for xx in a.get_possible_moves():
            b = a.make_move(xx)
            if b.over:
                ss.append(xx)
        if len(ss) == len(a.get_possible_moves()):
            ii.append(x)
        else:
            iii.append(x)


# The following code is used to generate stonhenge strings for __str__ method in
# StonehengeState class.


LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
           'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']


def stone_generator(n):
    """
    Generate a Stonehenge.
    """
    copy = LETTERS[:]
    empty = []
    h = n
    i = 2
    get_begin_rows(empty, h)
    while i < h+2:
        empty_1 = []
        x = 0
        while x < i - 1:
            empty_1.append([copy.pop(0), ' ', '-', ' '])
            x += 1
        if i == (h + 1):
            empty_1.append([copy.pop(0)])
        else:
            empty_1.append([copy.pop(0), ' ', ' ', ' ', '@'])

        empty.append(insert_space(sum(empty_1, []), h, i))
        if i != h + 1:
            empty.append(get_diagonals(h, i))

        i += 1
    empty.append([' ', ' ', ' ', ' ', ' '] + get_diagonal_2(h))

    empty_2 = []
    for x in range(h - 1):
        empty_2.append([copy.pop(0), ' ', '-', ' '])
    empty_2.append([copy.pop(0), ' ', ' ', ' ', '@'])
    empty.append([' ', ' ', '@', ' ', '-', ' '] + sum(empty_2, []))
    get_ending_rows(empty, h)
    empty[-1] = empty[-1][:-3]
    empty[-2] = empty[-2][:-3]
    return empty


def get_ending_rows(alist, size):
    """
    Add ending rows to alist.
    """
    sta = ['\\', ' ', ' ', ' ']
    alist.append([' ', ' ', ' ', ' ', ' ', ' ', ' '] +
                 sum([sta for i in range(size)], []))
    sta_1 = ['@', ' ', ' ', ' ']
    alist.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '] +
                 sum([sta_1 for ii in range(size)], []))


def get_begin_rows(alist, size):
    """
    Modify alist by adding beginning row to it.
    """
    alist.append([' ' for i in range(2*size + 4)] + ['@', ' ', ' ', ' ', '@'])
    alist.append([' ' for s in range(2*size + 3)] + ['/', ' ', ' ', ' ', '/'])


def get_diagonal_2(size):
    """
    Return a list of proper diagonals.
    """
    empty = []
    x = 0
    while x < size:
        empty.append(['\\', ' ', '/', ' '])
        x += 1
    empty.append(['\\'])
    return sum(empty, [])


def insert_space(alist, size, row):
    """
    Return a list with proper white spaces inserted to alist based on row and
    size.
    """
    num = 2*(size-(row-1))
    empty = []
    x = 0
    while x < num:
        empty.append(' ')
        x += 1
    empty_1 = [empty, ['@', ' ', '-', ' '], alist]
    return sum(empty_1, [])


def get_diagonals(size, row):
    """
    Return a diagonal base on size and number of cells in the row.
    """
    white_space = 3 + 2*(size - (row - 1))
    empty = []
    x = 0
    while x < white_space:
        empty.append([' '])
        x += 1
    standard = ['/', ' ', '\\', ' ']
    x = 0
    while x < row:
        empty.append(standard)
        x += 1
    empty.append(['/'])
    return sum(empty, [])


if __name__ == '__main__':
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
