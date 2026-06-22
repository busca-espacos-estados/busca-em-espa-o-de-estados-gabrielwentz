# -*- coding: utf-8 -*-
from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

class BFS(BaseSearch):
    def search(self, initial: State) -> SearchResult:
        
        goal_board = (1, 2, 3, 8, 0, 4, 7, 6, 5)
        
        frontier = deque([initial])
        explored = set()
        frontier_set = {initial}
        
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1
        
        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            current_state = frontier.popleft()
            frontier_set.remove(current_state)
            
            if current_state.board == goal_board:
                return SearchResult(
                    solution=current_state,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=len(current_state.actions())
                )
            
            explored.add(current_state.board)
            nodes_expanded += 1
            
            for child in current_state.neighbors():
                if child.board not in explored and child not in frontier_set:
                    frontier.append(child)
                    frontier_set.add(child)
                    nodes_generated += 1
                    
        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0
        )
