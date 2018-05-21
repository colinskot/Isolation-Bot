"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random as r


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def terminal_test(game):
    """
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    Returns
    -------
    boolean
        Whether or not there are moves left for the current player. If a
        player does not have a move left, game is over, other player wins.
    """
    # check if there are moves left
    return not bool(game.get_legal_moves())


def timeout_check(self):
    """
    Checks to see if the TIMER_THRESHOLD has been reached.
    """
    if self.time_left() < self.TIMER_THRESHOLD:
        raise SearchTimeout()


def check_winner(game, player):
    """
    Return best score if move wins game.
    Return worst score if move loses game.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")


# def heuristic_1(game, player):
#     pass


def custom_score(game, player):
    """
    A weighted heuristic which does not give a high score early on
    in the game. However, as the game goes on, decreasing the opp_moves
    becomes more valuable. The reason for this is that the board early on is
    very symmetrical, so having different moves does not matter as much.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.

    Best Score
    ----------
    Match #  Opponent   AB_Improved  AB_Custom
                        Won | Lost   Won | Lost
    1       Random      16  |   4    18  |   2
    2       MM_Open     12  |   8    11  |   9
    3      MM_Center    14  |   6    15  |   5
    4     MM_Improved    8  |  12    11  |   9
    5       AB_Open      9  |  11    12  |   8
    6      AB_Center    13  |   7    14  |   6
    7     AB_Improved    8  |  12    12  |   8
   -----------------------------------------------
           Win Rate:      57.1%        66.4%
    """
    check_winner(game, player)

    # useful attributes
    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    total = my_moves + opp_moves

    # to insure no division by 0
    if total == 0:
        total += 1

    # appreciating weight
    weight = 1/total

    # become more aggressive as the game goes on
    score = float(my_moves - (weight * opp_moves))

    return score


def custom_score_2(game, player):
    """
    Linear combination.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    check_winner(game, player)

    # useful attributes
    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    mobility = my_moves
    relative_mobility = my_moves - opp_moves

    # linear combination score
    score = float(mobility + relative_mobility)

    return score


def custom_score_3(game, player):
    """
    Fixed weight to reward decreasing opponents moves.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    check_winner(game, player)

    # moves left for each player
    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    # consistently decrease opponents moves
    score = float(my_moves - (1.25 * opp_moves))

    return score


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            print("Search has timedout, returning best move: " + str(best_move))

        # Return the best move from the last completed search iteration
        return best_move


    def max_value(self, game, depth):

        timeout_check(self)

        # recursive calls decrement depth until it reaches 0 or terminal_test
        if depth <= 0 or terminal_test(game):
            return self.score(game, self)

        v = float('-inf')

        # max in node, update depth
        for m in game.get_legal_moves():
            v = max(v, self.min_value(game.forecast_move(m), depth - 1))
        return v


    def min_value(self, game, depth):

        timeout_check(self)

        # recursive calls decrement depth until it reaches 0 or terminal_test
        if depth <= 0 or terminal_test(game):
            return self.score(game, self)

        v = float('inf')

        # min in node, update depth
        for m in game.get_legal_moves():
            v = min(v, self.max_value(game.forecast_move(m), depth - 1))
        return v


    def minimax(self, game, depth):
        """
        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        timeout_check(self)

        best_score = float('-inf')

        legal_moves = game.get_legal_moves()

        # no legal moves left
        if not legal_moves:
            return (-1, -1)
        # best move default (first available legal move)
        best_move = legal_moves[0]

        # all possible actions contrained by depth
        for m in game.get_legal_moves():
            v = self.min_value(game.forecast_move(m), depth - 1)
            if v > best_score:
                best_score = v
                best_move = m

        return best_move


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left # update time left

        best_move = (-1, -1)

        # The try/except block will automatically catch the exception
        # raised when the timer is about to expire.
        try:
            search_depth = 0 # limited iterative deepening, start at 0
            while True:
                move = self.alphabeta(game, search_depth)
                if move == (-1, -1):
                    return best_move
                else:
                    best_move = move
                search_depth += 1 # increment until timeout

        except SearchTimeout:
            return best_move # return current best move on timeout

        # return the best move from the last completed search iteration
        return best_move

    def max_value(self, game, alpha, beta, depth):

        timeout_check(self)

        # recursive calls decrement depth until it reaches 0 or terminal_test
        if depth <= 0 or terminal_test(game):
            return self.score(game, self)

        v = float('-inf')

        # max in node, update depth/alpha
        for m in game.get_legal_moves():
            v = max(v, self.min_value(game.forecast_move(m), alpha, beta, depth - 1))
            # check upper bound
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v


    def min_value(self, game, alpha, beta, depth):

        timeout_check(self)

        # recursive calls decrement depth until it reaches 0 or terminal_test
        if depth <= 0 or terminal_test(game):
            return self.score(game, self)

        v = float('inf')

        # min in node, update depth/beta
        for m in game.get_legal_moves():
            v = min(v, self.max_value(game.forecast_move(m), alpha, beta, depth - 1))
            # check lower bound
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """
        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md


        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        timeout_check(self)

        best_score = float('-inf')

        legal_moves = game.get_legal_moves()

        # no legal moves left
        if not legal_moves:
            return (-1, -1)
        # best move default (first available legal move)
        best_move = legal_moves[0]

        # all possible actions constrained by depth/alpha/beta
        for m in game.get_legal_moves():
            v = self.min_value(game.forecast_move(m), alpha, beta, depth - 1)
            if v > best_score:
                best_score = v
                best_move = m

        return best_move
