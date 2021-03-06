"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def num_moves(game, player):
    # calculate number of legal moves
    if game.is_loser(player):
       return float("-inf")

    if game.is_winner(player):
       return float("inf")

    return float(len(game.get_legal_moves()))

def moves_diff2(game, player):
    #calculate #moves of player - 2*#moves of opponent. 
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(own_moves - 2*opp_moves)

def moves_diff3(game, player):
    #calculate #moves of player - 2*#moves of opponent. 
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(own_moves - 2*opp_moves)

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

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

    # TODO: finish this function!
    return moves_diff2(game, player)

    raise NotImplementedError


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

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

        def move_function(method, depth):
            if self.method == 'alphabeta':
                return self.alphabeta(game,depth)[1]
            else:
                return self.minimax(game,depth)[1]

        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            
            if (game.width/2, game.height/2) in game.get_blank_spaces():
                return (game.width/2, game.height/2)

            if self.iterative:
                # perform iterative deepening
                size = game.width*game.height
                move = (-1,-1)
                for i in range(1, size): 
                    move = move_function(self.method, i)                      
            else:
                # perform depth-limited search
                move = move_function(self.method, self.search_depth)

        except Timeout:
            # Handle any actions required at timeout, if necessary
            pass

        # Return the best move from the last completed search iteration
        return move

        raise NotImplementedError

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()
        
        # TODO: finish this function!
        
        # get current active player.
        player = game.active_player

        # Return Utility if current state is terminal state or max_depth
        def max_value(game, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise Timeout()
            # Implement min-value search
            # get legal moves and inititate the maximum value, position tuptle
            moves, val = game.get_legal_moves(), (float("-inf"),(-1,-1))
            # terminate state or current depth is greater than or equal to search_depth
            if not moves or depth <= 0:  return (self.score(game,player), (-1,-1))       
            # in the legal moves, find the maximum value
            for m in moves:
                next_state = game.forecast_move(m)
                # For minimax function            
                val = max(val, (min_value(next_state, depth-1)[0],m))

            return val

        def min_value(game, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise Timeout()
            # Implement min-value search   
            # get legal moves and inititate the minimum value, position tuptle
            moves, val = game.get_legal_moves(), (float("inf"),(-1,-1))
            # terminate state or current depth is greater than or equal to search_depth
            if not moves or depth <= 0:  return (self.score(game,player), (-1,-1))
            # in the legal moves, find the minimum value
            for m in moves: 
                # For minimax function
                next_state = game.forecast_move(m)
                val = min(val, (max_value(next_state, depth-1)[0],m))

            return val
      
        # for searching max value
        if maximizing_player:
            # return the move that maximize the min_val
            return max_value(game, depth)
        # for searching min value
        else:
            # return the move that minimize the max_val
            return min_value(game, depth)
            
        
        
        raise NotImplementedError


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

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

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # get current active player.
        player = game.active_player

        def ab_max_value(game, depth, alpha, beta):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise Timeout()
            
            # get legal moves and inititate the maximum value, position tuptle
            moves, val = game.get_legal_moves(), (float("-inf"),(-1,-1))  
            # terminate state or current depth is greater than or equal to search_depth
            if not moves or depth <= 0:  return (self.score(game,player),(-1,-1))
            # in the legal moves, find the maximum value
            for m in moves:
                next_state = game.forecast_move(m)    
                val = max(val, (ab_min_value(next_state, depth-1, alpha, beta)[0], m))
                if val[0] >= beta: return val
                alpha = max(alpha, val[0])
            return val

        def ab_min_value(game, depth, alpha, beta):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise Timeout()

            # get legal moves and inititate the minimum value, position tuptle
            moves, val = game.get_legal_moves(), (float("inf"),(-1,-1))      
            # terminate state or current depth is greater than or equal to search_depth
            if not moves or depth <= 0:  return (self.score(game,player),(-1,-1))
            # in the legal moves, find the minimum value
            for m in moves: 
                # For minimax function
                next_state = game.forecast_move(m)
                val = min(val, (ab_max_value(next_state, depth-1, alpha, beta)[0],m))
                if val[0] <= alpha: return val
                beta = min(beta, val[0])
            return val

        
       
        return ab_max_value(game, depth, alpha, beta)
        

              
        raise NotImplementedError


    

    
