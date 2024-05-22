# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys, copy
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class PipeManiaState:
    state_id = 0

    def __init__(self, board, position):
        self.board = board
        self.position = position
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    def __init__(self, board_data, board_size):
        """""if isinstance(board_data[0], str):  # list of strings
            self.board = [list(row) for row in board_data]
        else:
            self.board = board_data"""
        self.board = board_data
        self.size = board_size

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str): # type: ignore
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        above = self.board[row - 1][col] if row > 0 else None
        below = self.board[row + 1][col] if row < len(self.board) - 1 else None
        return above, below

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str): # type: ignore
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        left = self.board[row][col - 1] if col > 0 else None
        right = self.board[row][col + 1] if col < len(self.board[row]) - 1 else None
        return left, right

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe.py < test-01.txt

            > from sys import stdin
            > line = stdin.readline().split()
        """
        board_data = []
        for line in sys.stdin:
            board_data.append(line.strip().split())
        board_size = len(board_data[0])
        return Board(board_data, board_size)

    def print(self):
        """Imprime o tabuleiro."""
        for row in self.board:
            for value in row:
                print(value, end=' ')
            print()

    def get_actions(self, position: int):
        
        board = self.board
        size = len(board)

        row = (position-1) // size
        col = (position-1) % size

        piece = board[row][col]

        normal_actions = [(position, 'clockwise'), (position, 'counter'), (position, 'inverse'), (position, 'keep')]

        abnormal_actions = [(position, 'clockwise'), (position, 'keep')]


        if piece[0] != 'L':
            return normal_actions
        else:
            return abnormal_actions
        
    def set_value(self, position: int, change: str, size: int):
        
        row = (position-1) // size
        col = (position-1) % size

        piece = self.board[row][col]

        if change == 'keep':
            return
        
        if piece[0] == 'L':
            if change == 'clockwise':
                if piece[1] == 'H':
                    self.board[row][col] = 'L' + 'V'
                else:
                    self.board[row][col] = 'L' + 'H'

        else:
            if change == 'clockwise':
                if piece[1] == 'C':
                    self.board[row][col] = piece[0] + 'D'
                elif piece[1] == 'B':
                    self.board[row][col] = piece[0] + 'E'
                elif piece[1] == 'E':
                    self.board[row][col] = piece[0] + 'C'
                elif piece[1] == 'D':
                    self.board[row][col] = piece[0] + 'B'

            elif change == 'counter':
                if piece[1] == 'C':
                    self.board[row][col] = piece[0] + 'E'
                elif piece[1] == 'B':
                    self.board[row][col] = piece[0] + 'D'
                elif piece[1] == 'E':
                    self.board[row][col] = piece[0] + 'B'
                elif piece[1] == 'D':
                    self.board[row][col] = piece[0] + 'C'

            elif change == 'inverse':
                if piece[1] == 'C':
                    self.board[row][col] = piece[0] + 'B'
                elif piece[1] == 'B':
                    self.board[row][col] = piece[0] + 'C'
                elif piece[1] == 'E':
                    self.board[row][col] = piece[0] + 'D'
                elif piece[1] == 'D':
                    self.board[row][col] = piece[0] + 'E'
    
    def to_list(self):
        pass
   
    # TODO: outros metodos da classe


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = board

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        
        actions = []
        position = state.position
        board = state.board
        size = board.size

        if position > size*size : # position > size*size
            return actions
        else:
            #possivelmente fazer algo aqui
            #board = Board(board_list)
            actions = board.get_actions(position)

            return actions

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        
        position = action[0]
        change = action[1]

        new_board = copy.copy(state.board)

        new_board.set_value(position, change) # verificar size

        #new_board_simplified = new_board.to_list()

        return PipeManiaState(new_board, state.position + 1)

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        
        board = state.board
        size = state.board.size

        connects_up = ['FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV']
        connects_down = ['FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV']
        connects_right = ['FD', 'BC', 'BB', 'BD', 'VB', 'VD', 'LH']
        connects_left = ['FE', 'BC', 'BB', 'BE', 'VC', 'VE', 'LH']

        for row in range(size):
            for col in range(size):
                if board.board[row][col] in connects_up:
                    if board.board[row+1][col] not in connects_down:
                        return False
                if board.board[row][col] in connects_down:
                    if board.board[row-1][col] not in connects_up:
                        return False
                if board.board[row][col] in connects_right:
                    if board.board[row][col+1] not in connects_left:
                        return False
                if board.board[row][col] in connects_left:
                    if board.board[row][col-1] not in connects_right:
                        return False
                    
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    
    board = Board.parse_instance()
    board.print()

    problem = PipeMania(board)
    #initial_state = (board, 1)
    result_state = depth_first_tree_search(problem)
    
    result_state.board.print()

    pass
