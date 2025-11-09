# Case Closed - Tron Lightbike Agent

A high-performance AI agent for competitive Tron Lightbike gameplay. This agent uses advanced pathfinding, territory control, and opponent prediction to outmaneuver opponents in a grid-based arena.

## Overview

The grid is your crime scene. Every move leaves evidence. Every turn could be your last.

This agent is designed to compete in head-to-head Tron matches where:
- **Arena Size**: 18 × 20 grid
- **Movement**: Each move leaves a permanent trail/barrier
- **Objective**: Survive longer than your opponent
- **Elimination**: Colliding with any trail (yours or opponent's) means instant elimination

## Agent Strategy

The agent employs multiple sophisticated strategies:

### 1. **Survival First**
- Calculates accessible space using BFS flood fill
- Prioritizes moves that maximize remaining territory
- Avoids moves that lead to dead ends

### 2. **Pathfinding**
- Uses A* algorithm to find optimal paths to open areas
- Identifies large open areas and navigates toward them
- Evaluates multiple potential routes

### 3. **Territory Control**
- Calculates territory advantage vs. opponent
- Tries to claim larger areas of the board
- Blocks opponent's access to open spaces

### 4. **Opponent Prediction**
- Tracks opponent's movement patterns
- Predicts likely opponent moves
- Attempts to block opponent's paths

### 5. **Safety Evaluation**
- Calculates distance to nearest walls
- Maintains safe distance from opponent
- Avoids corners early in the game

## Project Structure

```
tron/
├── agent.py              # Main agent implementation
├── pathfinder.py         # Pathfinding utilities (A*, BFS)
├── game_simulator.py     # Local testing simulator
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker container configuration
└── README.md            # This file
```

## Quick Start

### Local Testing

1. **Install dependencies** (if any):
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the simulator**:
   ```bash
   python game_simulator.py
   ```

3. **Test your agent**:
   ```python
   from game_simulator import TronSimulator
   import agent
   
   simulator = TronSimulator()
   result = simulator.play_game((10, 9), (9, 9))
   print(f"Game result: {result}")
   ```

### Docker Build (Recommended)

1. **Build the Docker image**:
   ```bash
   docker build -t tron-agent .
   ```

2. **Test the container**:
   ```bash
   docker run tron-agent
   ```

3. **Verify the agent loads**:
   The container should print "Agent loaded successfully"

## 📤 Submission Guidelines

Your submission must include:

-  **agent.py** - Main agent file (do not rename)
-  **requirements.txt** - All Python dependencies
-  **Dockerfile** - Container configuration (optional but recommended)
-  **Helper modules** - Any additional Python files imported by agent.py

### Key Requirements

-  **5GB Docker image limit** - Keep dependencies minimal
-  **CPU-only PyTorch** - GPU/CUDA builds are not allowed
-  **No TensorFlow/JAX** - Large ML libraries may be disallowed
-  **Test before submitting** - Ensure Docker image builds successfully

##  Agent Interface

The game engine calls the `get_move()` function in `agent.py`:

```python
def get_move(state: dict) -> str:
    """
    Main entry point for the game engine.
    
    Args:
        state: Dictionary containing:
            - my_position: (x, y) tuple
            - opponent_position: (x, y) tuple
            - board: 2D list (0=empty, 1=wall/trail)
            - boosts: List of available boosts (optional)
            - turns_remaining: Number of turns left (optional)
            - opponent_last_direction: Last direction (optional)
    
    Returns:
        str: Direction to move ('up', 'down', 'left', 'right')
    """
```

##  Customization

### Adjusting Strategy Weights

Edit `agent.py` in the `_evaluate_moves()` method to adjust strategy weights:

```python
# Current weights
score += accessible_space * 10      # Survival (highest priority)
score += safety_dist * 2            # Safety distance
score += territory * 3              # Territory control
score += path_score * 5             # Pathfinding
score += block_score * 2            # Opponent blocking
```

### Adding New Strategies

1. Add evaluation method to `TronAgent` class
2. Call it in `_evaluate_moves()`
3. Add weighted score to move evaluation

##  Testing

The `game_simulator.py` provides:

- **Single game simulation**: Test specific scenarios
- **Batch testing**: Run multiple games and get statistics
- **Visualization**: Print board state for debugging

### Example Test

```python
from game_simulator import test_agent

# Run 20 test games
test_agent(num_games=20)
```

##  Performance Tips

1. **Cache computations**: Reuse pathfinding results when possible
2. **Optimize early**: Test with time limits to avoid timeouts
3. **Modular code**: Keep decision logic separate from state parsing
4. **Test locally**: Verify agent works before submitting

##  Troubleshooting

### Docker Build Fails
- Check `requirements.txt` for invalid dependencies
- Ensure Dockerfile syntax is correct
- Verify base image is available

### Agent Times Out
- Reduce computation in `get_move()`
- Cache expensive calculations
- Optimize pathfinding algorithms

### Agent Makes Invalid Moves
- Check bounds validation in `_get_valid_moves()`
- Verify board state parsing
- Test with game simulator

##  License

This project is created for the Case Closed Tron competition.

##  Contributing

---

**Good luck, and may your agent solve the case before it's too late!** 🕵️‍♂️

