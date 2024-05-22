# Auxiliary functions

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

def all_connections_valid(board):
    """Verifica se todas as conexões no tabuleiro são válidas."""
    rows = len(board)
    cols = len(board[0])
    for row in range(rows):
        for col in range(cols):
            current_piece = board.get_value(row, col)
            neighbors = board.get_vizinhos(row, col)
            for neighbor, position in neighbors:
                if not can_connect(current_piece, (row, col), neighbor, position):
                    return False
    return True



def evaluate_action_potential(board, row, col, new_orientation):
    """ O objetivo desta funcao eh avaliar quantitativamente o efeito de uma ação (uma possível rotação de peça) 
    em termos de como essa ação melhora ou piora as conexões entre as peças no tabuleiro. 
    Isso é feito calculando a diferença no número de conexões válidas antes e depois da ação ser aplicada."""

    current_orientation = board[row][col]

    board[row][col] = new_orientation                       # Temporariamente aplica a nova orientação
    new_connections = count_connections(board, row, col)    # Calcula conexões para a nova orientação

    board[row][col] = current_orientation                       # Reverte para a orientação original
    current_connections = count_connections(board, row, col)    # Calcula conexões para a orientação atual

    return new_connections - current_connections  # Potencial é a diferença nas conexões


def count_connections(board, row, col):
    """Contar quantas conexões válidas uma peça específica tem com suas peças vizinhas no tabuleiro (cima, baixo, esquerda, direita)."""
    # 1º Identificar os Vizinhos: Para uma peça na posição (row, col), identificar as peças vizinhas 
    # 2º Verificar Conexões: Para cada uma dessas posições, verificar se a peça atual se pode conectar à peça vizinha com base na orientação das peças 
    total_connections = 0
    current_piece = board.get_value(row, col)
    neighbours = get_vizinhos(row, col, board)

    for neighbour, position in neighbours:
        if can_connect(current_piece, (row, col), neighbour, position):
            total_connections += 1

    return total_connections


def get_vizinhos(row, col, board):
    # rows = len(board)
    # cols = len(board[0])
    rows = board.get_num_rows()
    cols = board.get_num_rows()
    neighbors = []

    # Verifica se existe vizinho à esquerda
    if col > 0:
        neighbors.append((board[row][col-1], (row, col-1), 'left')) 
    # Verifica se existe vizinho à direita
    if col < cols - 1:
        neighbors.append((board[row][col+1], (row, col+1), 'right')) 
    # Verifica se existe vizinho acima
    if row > 0:
        neighbors.append((board[row-1][col], (row-1, col), 'up')) 
    # Verifica se existe vizinho abaixo
    if row < rows - 1:
        neighbors.append((board[row+1][col], (row+1, col), 'down')) 

    return neighbors


def can_connect(piece1, pos1, piece2, pos2):
    """Verifica se duas peças conectam.
    Retorna True se a conexão for válida, False caso contrário."""
    
    row1, col1 = pos1
    row2, col2 = pos2

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


# --------------------------- UNUSED ---------------------------

def get_possible_movements(row: int, col: int, piece: str, size: int):
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


def count_valid_connections(board):
    total_connections = 0
    for row in range(len(board.board)):
        for col in range(len(board.board[0])):
            total_connections += count_connections(board, row, col)
    return total_connections

# --------------------------- UNUSED ---------------------------

def all_connections_valid(self):
        """Verifica se todas as conexões no tabuleiro são válidas."""
        
        rows = self.get_num_rows()
        cols = self.get_num_rows()

        for row in range(rows):
            for col in range(cols):
                current_piece = self.get_value(row, col)
                neighbors = get_vizinhos(row, col)
                for neighbor, position in neighbors:
                    if not can_connect(current_piece, (row, col), neighbor, position):
                        return False
        return True

def get_possible_actions(self, position: int):
    """Retorna uma lista de ações possíveis para a peça na posição
    (row, col) do tabuleiro."""

    board = self.board
    size = self.size

    row = (position-1) // size
    col = (position-1) % size

    piece = board[row][col]

    if self.check_corner(row, col):
        
        if self.upper_left_corner(row, col):
            
            if piece[0] == 'F':
                if piece[1] == 'C':
                    return [(position, 'clockwise'), (position, 'inverse')]
                if piece[1] == 'B':
                    return [(position, 'counter'), (position, 'keep')]
                if piece [1] == 'E':
                    return [(position, 'counter'), (position, 'inverse')]
                if piece[1] == 'D':
                    return [(position, 'clockwise'), (position, 'keep')]
            
            if piece[0] == 'V':
                pass
                

def check_corner (self, row: int, col: int):
    """Verifica se a peça na posição (row, col) é um canto."""
    
    if row == 0 and col == 0:
        return True
    if row == 0 and col == self.size - 1:
        return True
    if row == self.size - 1 and col == 0:
        return True
    if row == self.size - 1 and col == self.size - 1:
        return True
    else:
        return False
    
def check_edge (self, row: int, col: int):
    """Verifica se a peça na posição (row, col) é uma borda."""

    if row == 0 and col != 0 and col != self.size - 1:
        return True
    
    if row == self.size - 1 and col != 0 and col != self.size - 1:
        return True
    
    if col == 0 and row != 0 and row != self.size - 1:
        return True
    
    if col == self.size - 1 and row != 0 and row != self.size - 1:
        return True
    else:
        return False
    
def upper_left_corner (self, row: int, col: int):
    """Verifica se a peça na posição (row, col) é um canto superior esquerdo."""
    
    if row == 0 and col == 0:
        return True
    else:
        return False
    
def upper_right_corner (self, row: int, col: int):
    """Verifica se a peça na posição (row, col) é um canto superior direito."""
    
    if row == 0 and col == self.size - 1:
        return True
    else:
        return False
    
def bottom_left_corner (self, row: int, col: int):
    """Verifica se a peça na posição (row, col) é um canto inferior esquerdo."""
    
    if row == self.size - 1 and col == 0:
        return True
    else:
        return False

def bottom_right_corner (self, row: int, col: int):
    """Verifica se a peça na posição (row, col) é um canto inferior direito."""
    
    if row == self.size - 1 and col == self.size - 1:
        return True
    else:
        return False