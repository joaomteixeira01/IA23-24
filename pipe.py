# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

#from aux_functions import *
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

    def set_value(self, row: int, col: int, new_piece: str) -> None:
        """Altera o valor na respetiva posição do tabuleiro."""

        self.board[row][col] = new_piece

    def get_length(self):
        """Returns the number of rows in the board."""
        return len(self.board)
    
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
    
    
    def evaluate_action_potential(self, row: int, col: int, new_orientation: str) -> int:
        """ O objetivo desta funcao eh avaliar quantitativamente o efeito de uma ação (uma possível rotação de peça) 
        em termos de como essa ação melhora ou piora as conexões entre as peças no tabuleiro. 
        Isso é feito calculando a diferença no número de conexões válidas antes e depois da ação ser aplicada."""

        current_orientation = self.board[row][col]

        self.board[row][col] = new_orientation                       # Temporariamente aplica a nova orientação
        new_connections = self.count_connections(row, col)    # Calcula conexões para a nova orientação

        self.board[row][col] = current_orientation                       # Reverte para a orientação original
        current_connections = self.count_connections(row, col)    # Calcula conexões para a orientação atual

        return new_connections - current_connections  # Potencial é a diferença nas conexões
    
    def count_connections(self, row, col) -> int:
        """Contar quantas conexões válidas uma peça específica tem com suas peças vizinhas no tabuleiro (cima, baixo, esquerda, direita)."""
        # 1º Identificar os Vizinhos: Para uma peça na posição (row, col), identificar as peças vizinhas 
        # 2º Verificar Conexões: Para cada uma dessas posições, verificar se a peça atual se pode conectar à peça vizinha com base na orientação das peças 
        total_connections = 0
    
        current_piece = (self.board[row][col], (row, col))
        neighbours = self.get_vizinhos(row, col)

        for neighbour in neighbours:
            if self.can_connect(current_piece, neighbour):
                total_connections += 1

        return total_connections
    
    def get_vizinhos(self, row, col) -> list:
        # rows = len(board)
        # cols = len(board[0])
        rows = self.get_length()
        cols = self.get_length()
        neighbours = []

        # Verifica se existe vizinho à esquerda
        if col > 0:
            neighbours.append((self.board[row][col-1], (row, col-1)))
        # Verifica se existe vizinho à direita
        if col < cols - 1:
            neighbours.append((self.board[row][col+1], (row, col+1)))
        # Verifica se existe vizinho acima
        if row > 0:
            neighbours.append((self.board[row-1][col], (row-1, col))) 
        # Verifica se existe vizinho abaixo
        if row < rows - 1:
            neighbours.append((self.board[row+1][col], (row+1, col))) 

        return neighbours
    
    def can_connect(self, piece1, neighbour) -> bool:
        """Verifica se duas peças conectam.
        Retorna True se a conexão for válida, False caso contrário."""
        
        pieces = {
            'F': {'C', 'B', 'E', 'D'},
            'B': {'C', 'B', 'E', 'D'},
            'V': {'C', 'B', 'E', 'D'},
            'L': {'V', 'H'}
        }

        connections = {
            # Nas ligacoes da peca F temos de retirar a ligacao F da lista
            'up': {'FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV'},
            'down': {'FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV'},
            'left': {'FD', 'BC', 'BB', 'BD', 'VB', 'VD', 'LH'},
            'right': {'FE', 'BC', 'BB', 'BE', 'VC', 'VE', 'LV'}
        }

        row1, col1 = piece1[1]
        row2, col2 = neighbour[1]
        piece2 = neighbour
        

        # Se as peças forem do tipo 'F', retorna False
        if piece1[0] == 'F' and piece2[0] == 'F':
            return False

        # Determinar a direção da conexão com base nas posições relativas
        if row1 == row2:
            if col2 == col1 + 1:
                direction = 'right'
            elif col2 == col1 - 1:
                direction = 'left'
            else:
                return False
        elif col1 == col2:
            if row2 == row1 + 1:
                direction = 'down'
            elif row2 == row1 - 1:
                direction = 'up'
            else:
                return False
        else:
            return False  # As peças não estão alinhadas horizontal ou verticalmente

        # Buscar as conexões possíveis para a peça1 na direção calculada
        p1_connections = connections.get(direction, set())

        # Caso piece1 seja F, remover a peca F das conexoes
        if piece1[0] == 'F': 
            p1_connections = [item for item in p1_connections if 'F' not in item]

        # Verificar se a combinação de tipo e orientação da peça2 é válida para a conexão
        if piece2 in p1_connections:
            return True

        return False
    
    def get_possible_movements(self, row: int, col: int, piece: str, size: int) -> list:
        """ funcao que vai retornar todos os possiveis movimentos de uma dada peca numa dada posicao
            movimentos que façam sentido, por exemplo, a peça F na posicao (0,0) nao faz sentido estar virada para C nem para E """

        

        possibilities = []
        p = piece[0]

        if row == 0:
            
            if col == 0:
                if p == 'F': possibilities.extend(['FD', 'FB'])
                if p == 'B': None
                if p == 'V': possibilities.append('VB')
                if p == 'L': None
            
            elif col > 0 and col < size - 1:
                if p == 'F': possibilities.extend(['FE', 'FD', 'FB'])
                if p == 'B': possibilities.append('BB')
                if p == 'V': possibilities.extend(['VB', 'VE'])
                if p == 'L': possibilities.append('LH')
            
            elif col == size - 1:
                if p == 'F': possibilities.extend(['FE', 'FB'])
                if p == 'B': None
                if p == 'V': possibilities.append('VE')
                if p == 'L': None
            
            else:
                # outside of board
                pass

        if row > 0 and row < size - 1:
            
            if col == 0:
                if p == 'F': possibilities.extend(['FC', 'FD', 'FB'])
                if p == 'B': possibilities.append('BD')
                if p == 'V': possibilities.extend(['VD', 'VB'])
                if p == 'L': possibilities.append('LV')
            
            elif col > 0 and col < size - 1:
                if p == 'F': possibilities.extend(['FE', 'FC', 'FD', 'FB'])
                if p == 'B': possibilities.extend(['BE', 'BC', 'BD', 'BB'])
                if p == 'V': possibilities.extend(['VE', 'VC', 'VD', 'VB'])
                if p == 'L': possibilities.extend(['LH', 'LV'])
            
            elif col == size - 1:
                if p == 'F': possibilities.extend(['FE', 'FB', 'FC'])
                if p == 'B': possibilities.append('BE')
                if p == 'V': possibilities.extend(['VC', 'VE'])
                if p == 'L': possibilities.append('LV')
            
            else:
                # outside of board
                pass

        if row == size - 1:
            
            if col == 0:
                if p == 'F': possibilities.extend(['FC', 'FD'])
                if p == 'B': None
                if p == 'V': possibilities.append('VD')
                if p == 'L': None
            
            elif col > 0 and col < size - 1:
                if p == 'F': possibilities.extend(['FE', 'FC', 'FD'])
                if p == 'B': possibilities.append('BC')
                if p == 'V': possibilities.extend(['VC', 'VD'])
                if p == 'L': possibilities.append('LH')
            
            elif col == size - 1:
                if p == 'F': possibilities.extend(['FE', 'FC'])
                if p == 'B': None
                if p == 'V': possibilities.append('VC')
                if p == 'L': None
            
            else:
                # outside of board
                pass

        # Remove a posicao atual da peca
        if piece in possibilities:
            possibilities.remove(piece)

        return possibilities
    
    def count_valid_connections(self) -> int:
        total_connections = 0
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                total_connections += self.count_connections(row, col)
        return total_connections
    
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
        actions0 = []
        actions1 = []
        actions2 = []
        size = state.board.get_length()

        for row in range(size):
            for col in range(size):
                piece = state.board.board[row][col]
                # Obter todas as orientações válidas para uma peça numa dada posição
                possible_orientations = state.board.get_possible_movements(row, col, piece, size) 
                for orientation in possible_orientations:
                    # Para cada movimento válido, calcula um potencial que meça o número de conexões válidas que são criadas ou melhoradas pela rotação da peça.
                    potential = state.board.evaluate_action_potential(row, col, orientation) 
                    if potential == 2:  # Filtra para manter apenas movimentos com potencial positivo
                        actions2.append((row, col, orientation))
                    elif potential == 1:
                        actions1.append((row, col, orientation))
                    elif potential == 0:
                        actions0.append((row, col, orientation))

        actions.extend(actions2)
        actions.extend(actions1)
        actions.extend(actions0)               
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
        
        size = state.board.get_length()   # Tamanho do tabuleiro

        connections = state.board.count_valid_connections()

        if connections == 2 * ((size * size) - 1):
            return True
        else:
            return False

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        #contar o número de peças que ainda não estão conectadas corretamente
        # A heurística é o inverso do número de conexões válidas, pois queremos maximizar as conexões
        
        connections = node.state.board.count_valid_connections()
        size = node.state.board.get_length()
        
        goal_connections = 2 * ((size * size) - 1)
        
        diff = goal_connections - connections
        print(diff)

        return diff

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
    result_state = astar_search(problem)
    
    result_state.board.print()

    # Usar uma técnica de procura para resolver a instância,
        # Temos de escolher umas das funcoes de procura em search.py
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
