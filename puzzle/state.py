# -*- coding: utf-8 -*-

class State:
    def __init__(self, board, parent=None, action=None):
        # Converte em tupla para garantir que seja imutável e possa ser adicionado em sets (hashable)
        self.board = tuple(board)  
        self.parent = parent       
        self.action = action       

    def neighbors(self):
        """Gera os estados filhos a partir do espaço vazio (0)"""
        children = []
        try:
            zero_index = self.board.index(0)
        except ValueError:
            zero_index = self.board.index('0')
            
        row, col = zero_index // 3, zero_index % 3
        
        # Movimentos permitidos para o espaço vazio
        moves = [
            (-1, 0, 'Cima'),    
            (1, 0, 'Baixo'),    
            (0, -1, 'Esquerda'),
            (0, 1, 'Direita')   
        ]
        
        for dr, dc, action_name in moves:
            new_row, new_col = row + dr, col + dc
            
            # Verifica se o movimento respeita os limites da matriz 3x3
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_zero_index = new_row * 3 + new_col
                
                # Faz a cópia e troca as posições
                new_board = list(self.board)
                new_board[zero_index], new_board[new_zero_index] = new_board[new_zero_index], new_board[zero_index]
                
                child_state = State(new_board, parent=self, action=action_name)
                children.append(child_state)
                
        return children

    def path(self):
        """Reconstrói a sequência de estados do inicial até este"""
        state_sequence = []
        current = self
        while current is not None:
            state_sequence.append(current)
            current = current.parent
        return state_sequence[::-1]

    def actions(self):
        """Retorna a sequência de ações usando path()"""
        state_path = self.path()
        return [state.action for state in state_path if state.action is not None]

    @property
    def cost(self) -> int:
        """Exigido pelo SearchResult: calcula o custo baseado na quantidade de ações"""
        return len(self.actions())

    def __eq__(self, other):
        return self.board == other.board if isinstance(other, State) else False

    def __hash__(self):
        return hash(self.board)

    def __repr__(self):
        # Desenha o tabuleiro de forma visual no console
        return f"+-------+\n| {self.board[0]} {self.board[1]} {self.board[2]} |\n| {self.board[3]} {self.board[4]} {self.board[5]} |\n| {self.board[6]} {self.board[7]} {self.board[8]} |\n+-------+"