"""
Local game simulator for testing the Tron agent.
This allows you to test your agent before submission.
"""

import random
import time
from typing import Tuple, List, Optional
import agent


class TronSimulator:
    """Simple game simulator for local testing."""
    
    def __init__(self, width: int = 20, height: int = 18):
        """
        Initialize simulator.
        
        Args:
            width: Board width (default 20)
            height: Board height (default 18)
        """
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.directions = {
            'up': (0, -1),
            'down': (0, 1),
            'left': (-1, 0),
            'right': (1, 0)
        }
    
    def reset(self, my_start: Tuple[int, int], opp_start: Tuple[int, int]):
        """
        Reset the game board.
        
        Args:
            my_start: Starting position for our agent (x, y)
            opp_start: Starting position for opponent (x, y)
        """
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.my_pos = my_start
        self.opp_pos = opp_start
        self.my_trail = [my_start]
        self.opp_trail = [opp_start]
        self.board[my_start[1]][my_start[0]] = 1
        self.board[opp_start[1]][opp_start[0]] = 1
        self.turn = 0
        self.game_over = False
        self.winner = None
    
    def get_state(self) -> dict:
        """
        Get current game state for agent.
        
        Returns:
            Dictionary containing game state
        """
        return {
            'my_position': self.my_pos,
            'opponent_position': self.opp_pos,
            'board': [row[:] for row in self.board],
            'boosts': [],
            'turns_remaining': 1000 - self.turn,
            'opponent_last_direction': getattr(self, 'opp_last_dir', None)
        }
    
    def is_valid_move(self, position: Tuple[int, int], direction: str) -> bool:
        """
        Check if a move is valid.
        
        Args:
            position: Current position (x, y)
            direction: Direction to move
        
        Returns:
            True if move is valid
        """
        if direction not in self.directions:
            return False
        
        dx, dy = self.directions[direction]
        new_x, new_y = position[0] + dx, position[1] + dy
        
        # Check bounds
        if new_x < 0 or new_x >= self.width or new_y < 0 or new_y >= self.height:
            return False
        
        # Check if cell is empty
        if self.board[new_y][new_x] == 1:
            return False
        
        return True
    
    def make_move(self, my_direction: str, opp_direction: Optional[str] = None) -> str:
        """
        Make a move for both agents.
        
        Args:
            my_direction: Our agent's move direction
            opp_direction: Opponent's move direction (None for random/CPU)
        
        Returns:
            Game result: 'win', 'lose', 'draw', or 'continue'
        """
        if self.game_over:
            return self.winner
        
        self.turn += 1
        
        # Get opponent move (random if not provided)
        if opp_direction is None:
            valid_opp_moves = [
                d for d in self.directions.keys() 
                if self.is_valid_move(self.opp_pos, d)
            ]
            opp_direction = random.choice(valid_opp_moves) if valid_opp_moves else 'up'
        
        self.opp_last_dir = opp_direction
        
        # Check if moves are valid
        my_valid = self.is_valid_move(self.my_pos, my_direction)
        opp_valid = self.is_valid_move(self.opp_pos, opp_direction)
        
        # Calculate new positions
        my_dx, my_dy = self.directions[my_direction]
        my_new_pos = (self.my_pos[0] + my_dx, self.my_pos[1] + my_dy)
        
        opp_dx, opp_dy = self.directions[opp_direction]
        opp_new_pos = (self.opp_pos[0] + opp_dx, self.opp_pos[1] + opp_dy)
        
        # Check collisions
        my_collision = not my_valid or self.board[my_new_pos[1]][my_new_pos[0]] == 1
        opp_collision = not opp_valid or self.board[opp_new_pos[1]][opp_new_pos[0]] == 1
        
        # Check if agents collide with each other
        if my_new_pos == opp_new_pos:
            self.game_over = True
            self.winner = 'draw'
            return 'draw'
        
        # Check if we move into opponent's new position (head-on collision)
        if my_new_pos == self.opp_pos and opp_new_pos == self.my_pos:
            self.game_over = True
            self.winner = 'draw'
            return 'draw'
        
        # Handle collisions
        if my_collision and opp_collision:
            self.game_over = True
            self.winner = 'draw'
            return 'draw'
        elif my_collision:
            self.game_over = True
            self.winner = 'lose'
            return 'lose'
        elif opp_collision:
            self.game_over = True
            self.winner = 'win'
            return 'win'
        
        # Update positions and board
        self.my_pos = my_new_pos
        self.opp_pos = opp_new_pos
        self.my_trail.append(self.my_pos)
        self.opp_trail.append(self.opp_pos)
        self.board[self.my_pos[1]][self.my_pos[0]] = 1
        self.board[self.opp_pos[1]][self.opp_pos[0]] = 1
        
        return 'continue'
    
    def play_game(self, my_start: Tuple[int, int], opp_start: Tuple[int, int], 
                  max_turns: int = 1000, verbose: bool = True) -> str:
        """
        Play a full game.
        
        Args:
            my_start: Our starting position
            opp_start: Opponent starting position
            max_turns: Maximum number of turns
            verbose: Print game progress
        
        Returns:
            Game result: 'win', 'lose', or 'draw'
        """
        self.reset(my_start, opp_start)
        
        if verbose:
            print(f"Starting game: My agent at {my_start}, Opponent at {opp_start}")
        
        while not self.game_over and self.turn < max_turns:
            # Get our agent's move
            state = self.get_state()
            my_move = agent.get_move(state)
            
            # Make move
            result = self.make_move(my_move)
            
            if verbose and self.turn % 50 == 0:
                print(f"Turn {self.turn}: My move: {my_move}, Result: {result}")
            
            if result != 'continue':
                break
        
        if self.game_over:
            if verbose:
                print(f"Game over after {self.turn} turns: {self.winner}")
            return self.winner
        else:
            if verbose:
                print(f"Game ended after {max_turns} turns (max reached)")
            return 'draw'
    
    def print_board(self):
        """Print the current board state."""
        print("\n" + "=" * (self.width * 2 + 1))
        for y in range(self.height):
            row = "|"
            for x in range(self.width):
                if (x, y) == self.my_pos:
                    row += "A|"
                elif (x, y) == self.opp_pos:
                    row += "B|"
                elif self.board[y][x] == 1:
                    row += "#|"
                else:
                    row += " |"
            print(row)
        print("=" * (self.width * 2 + 1) + "\n")


def test_agent(num_games: int = 10):
    """
    Test the agent against a random opponent.
    
    Args:
        num_games: Number of games to play
    """
    simulator = TronSimulator()
    results = {'win': 0, 'lose': 0, 'draw': 0}
    
    print(f"Testing agent for {num_games} games...")
    print("=" * 50)
    
    for i in range(num_games):
        # Random starting positions
        my_start = (random.randint(5, 14), random.randint(5, 12))
        opp_start = (random.randint(5, 14), random.randint(5, 12))
        
        # Ensure they're not too close
        while abs(my_start[0] - opp_start[0]) + abs(my_start[1] - opp_start[1]) < 5:
            opp_start = (random.randint(5, 14), random.randint(5, 12))
        
        result = simulator.play_game(my_start, opp_start, verbose=False)
        results[result] += 1
        
        if (i + 1) % 5 == 0:
            print(f"Games played: {i + 1}/{num_games}")
            print(f"  Wins: {results['win']}, Losses: {results['lose']}, Draws: {results['draw']}")
    
    print("=" * 50)
    print("Final Results:")
    print(f"  Wins: {results['win']} ({results['win']/num_games*100:.1f}%)")
    print(f"  Losses: {results['lose']} ({results['lose']/num_games*100:.1f}%)")
    print(f"  Draws: {results['draw']} ({results['draw']/num_games*100:.1f}%)")
    print(f"  Win Rate: {results['win']/(num_games-results['draw'])*100:.1f}% (excluding draws)")


if __name__ == "__main__":
    # Run tests
    test_agent(num_games=20)
    
    # Example single game
    print("\n" + "=" * 50)
    print("Example Game:")
    simulator = TronSimulator()
    simulator.play_game((10, 9), (9, 9), max_turns=100, verbose=True)
    simulator.print_board()

