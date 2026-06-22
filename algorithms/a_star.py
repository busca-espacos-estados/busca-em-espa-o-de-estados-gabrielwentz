# -*- coding: utf-8 -*-
import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        
        distance = 0
        
        # Mapeamento atualizado para refletir o objetivo (1 2 3 / 8 0 4 / 7 6 5)
        goal_positions = {
            1: (0, 0), 2: (0, 1), 3: (0, 2),
            8: (1, 0), 0: (1, 1), 4: (1, 2),
            7: (2, 0), 6: (2, 1), 5: (2, 2)
        }
        
        for index, value in enumerate(state.board):
            if value != 0:  
                current_row, current_col = index // 3, index % 3
                goal_row, goal_col = goal_positions[value]
                distance += abs(current_row - goal_row) + abs(current_col - goal_col)
                
        return distance

    def search(self, initial: State) -> SearchResult:
        goal_board = (1, 2, 3, 8, 0, 4, 7, 6, 5)
        
        frontier = []
        counter = 0
        
        h_initial = self.heuristic(initial)
        heapq.heappush(frontier, (0 + h_initial, counter, initial))
        
        g_score = {initial.board: 0}
        explored = set()
        
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1
        
        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            f_curr, _, current_state = heapq.heappop(frontier)
            
            if current_state.board == goal_board:
                return SearchResult(
                    solution=current_state,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=len(current_state.actions())
                )
            
            if current_state.board in explored:
                continue
                
            explored.add(current_state.board)
            nodes_expanded += 1
            current_g = g_score[current_state.board]
            
            for child in current_state.neighbors():
                if child.board in explored:
                    continue
                    
                tentative_g = current_g + 1
                if child.board not in g_score or tentative_g < g_score[child.board]:
                    g_score[child.board] = tentative_g
                    f_child = tentative_g + self.heuristic(child)
                    counter += 1
                    heapq.heappush(frontier, (f_child, counter, child))
                    nodes_generated += 1
                    
        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0
        )
