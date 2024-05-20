# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

from aux_functions import *
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

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe

    def is_goal(self):
        # Criar uma funcao all_connections_valid que verifique se todas as conecçoes sao validas
        return all_connections_valid(self.board)


class Board:
    """Representação interna de um tabuleiro de PipeMania."""
    def __init__(self, board_data):
        self.board = board_data

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str): # type: ignore
        """Devolve os valores imediatamente acima e abaixo, respectivamente."""
        above = self.board[row - 1][col] if row > 0 else None
        below = self.board[row + 1][col] if row < len(self.board) - 1 else None
        return above, below

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str): # type: ignore
        """Devolve os valores imediatamente à esquerda e à direita, respectivamente."""
        left = self.board[row][col - 1] if col > 0 else None
        right = self.board[row][col + 1] if col < len(self.board[row]) - 1 else None
        return left, right

    def print(self):
        """Imprime o tabuleiro."""
        for row in self.board:
            for value in row:
                print(value, end=' ')
            print()

    def set_value(self, row: int, col: int, rotation: bool) -> None:
        """Altera o valor na respetiva posição do tabuleiro."""

        piece = self.get_value(row, col)

        if piece[0] == 'L':
            if piece[1] == 'H':
                piece = piece[0] + 'V'
            else:
                piece = piece[0] + 'H'
        else:
            if piece[1] == 'C':
                if rotation == True:
                    piece = piece[0] + 'D'
                else:
                    piece = piece[0] + 'E'
            elif piece[1] == 'D':
                if rotation == True:
                    piece = piece[0] + 'B'
                else:
                    piece = piece[0] + 'C'
            elif piece[1] == 'B':
                if rotation == True:
                    piece = piece[0] + 'E'
                else:
                    piece = piece[0] + 'D'
            elif piece[1] == 'E':
                if rotation == True:
                    piece = piece[0] + 'C'
                else:
                    piece = piece[0] + 'B'
            
        self.board[row][col] = piece

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
        return Board(board_data)
    
    # TODO: outros metodos da classe


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = PipeManiaState(board)
    
    """def actions(self, state: PipeManiaState):
        Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento.

        actions = []
        board = state.board.board
        

        # Iterar por cada posição do tabuleiro
        for row in range(len(board)):
            for col in range(len(board[row])):
                # Para cada peça, adicionar a ação 
                actions.extend(get_possible_movements(row, col, board[row][col]))
                # Uso do extend em vez de append, pois se for mais que um elemento o append n vai funcionar bem

        return actions"""
    
    def actions(self, state: PipeManiaState):
        """ Actions modificada para incluir a avaliacao do potencial e selecionar as acoes com potencial positivo """
        actions = []
        board = state.board.board

        for row in range(len(board)):
            for col in range(len(board[row])):
                piece = board[row][col]
                # Obter todas as orientações válidas para uma peça numa dada posição
                possible_orientations = get_possible_movements(row, col, piece) 
                for orientation in possible_orientations:
                    # Para cada movimento válido, calcula um potencial que meça o número de conexões válidas que são criadas ou melhoradas pela rotação da peça.
                    potential = evaluate_action_potential(board, row, col, orientation) 
                    if potential > 0:  # Filtra para manter apenas movimentos com potencial positivo
                        actions.append((row, col, orientation))
                        
        return actions

    

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        new_board = copy.deepcopy(state.board)

        new_board.set_value(action[0], action[1], action[2])

        new_state = PipeManiaState(new_board)

        return new_state

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        #contar o número de peças que ainda não estão conectadas corretamente
        # TODO
        # A heurística é o inverso do número de conexões válidas, pois queremos maximizar as conexões
        return -count_valid_connections(node.state.board)
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    board = Board.parse_instance()
    board.print()
    
    #print(board.adjacent_vertical_values(0, 0))
    #print(board.adjacent_horizontal_values(0, 0))
    #print(board.adjacent_vertical_values(1, 1))
    #print(board.adjacent_horizontal_values(1, 1))

    problem = PipeMania(board)
    initial_state = PipeManiaState(board)
    print(initial_state.board.get_value(2, 2))
    result_state = problem.result(initial_state, (2, 2, True))
    print(result_state.board.get_value(2, 2))
    
    result_state.board.print()

    # Usar uma técnica de procura para resolver a instância,
        # Temos de escolher umas das funcoes de procura em search.py
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
