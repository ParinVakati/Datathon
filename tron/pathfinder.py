"""
Pathfinding utilities for Tron agent.
Provides A* and BFS algorithms for navigation.
"""

from collections import deque
from typing import List, Tuple, Optional, Set
from heapq import heappush, heappop


class Pathfinder:
    """Pathfinding algorithms for grid navigation."""
    
    def __init__(self, width: int = 20, height: int = 18):
        """
        Initialize pathfinder.
        
        Args:
            width: Board width
            height: Board height
        """
        self.width = width
        self.height = height
        self.directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    
    def bfs(
        self, 
        start: Tuple[int, int], 
        goal: Tuple[int, int],
        board: List[List[int]]
    ) -> Optional[List[Tuple[int, int]]]:
        """
        Breadth-first search to find shortest path.
        
        Args:
            start: Starting position (x, y)
            goal: Goal position (x, y)
            board: 2D board (0=empty, 1=wall)
        
        Returns:
            List of positions forming path, or None if no path exists
        """
        if start == goal:
            return [start]
        
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            (x, y), path = queue.popleft()
            
            for dx, dy in self.directions:
                new_x, new_y = x + dx, y + dy
                new_pos = (new_x, new_y)
                
                if new_pos == goal:
                    return path + [goal]
                
                if (new_pos not in visited and 
                    0 <= new_x < self.width and 
                    0 <= new_y < self.height and
                    board[new_y][new_x] == 0):
                    visited.add(new_pos)
                    queue.append((new_pos, path + [new_pos]))
        
        return None
    
    def a_star(
        self, 
        start: Tuple[int, int], 
        goal: Tuple[int, int],
        board: List[List[int]]
    ) -> Optional[List[Tuple[int, int]]]:
        """
        A* pathfinding algorithm.
        
        Args:
            start: Starting position (x, y)
            goal: Goal position (x, y)
            board: 2D board (0=empty, 1=wall)
        
        Returns:
            List of positions forming path, or None if no path exists
        """
        def heuristic(pos: Tuple[int, int]) -> int:
            """Manhattan distance heuristic."""
            return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
        
        if start == goal:
            return [start]
        
        open_set = [(0, start)]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start)}
        visited = set()
        
        while open_set:
            current_f, current = heappop(open_set)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            if current == goal:
                # Reconstruct path
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                return path[::-1]
            
            x, y = current
            for dx, dy in self.directions:
                new_x, new_y = x + dx, y + dy
                neighbor = (new_x, new_y)
                
                if (0 <= new_x < self.width and 
                    0 <= new_y < self.height and
                    board[new_y][new_x] == 0):
                    
                    tentative_g = g_score.get(current, float('inf')) + 1
                    
                    if tentative_g < g_score.get(neighbor, float('inf')):
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g
                        f_score[neighbor] = tentative_g + heuristic(neighbor)
                        heappush(open_set, (f_score[neighbor], neighbor))
        
        return None
    
    def flood_fill(
        self, 
        start: Tuple[int, int], 
        board: List[List[int]]
    ) -> Set[Tuple[int, int]]:
        """
        Flood fill to find all connected empty cells.
        
        Args:
            start: Starting position (x, y)
            board: 2D board (0=empty, 1=wall)
        
        Returns:
            Set of all reachable positions
        """
        visited = set()
        queue = deque([start])
        visited.add(start)
        
        while queue:
            x, y = queue.popleft()
            
            for dx, dy in self.directions:
                new_x, new_y = x + dx, y + dy
                new_pos = (new_x, new_y)
                
                if (new_pos not in visited and 
                    0 <= new_x < self.width and 
                    0 <= new_y < self.height and
                    board[new_y][new_x] == 0):
                    visited.add(new_pos)
                    queue.append(new_pos)
        
        return visited

