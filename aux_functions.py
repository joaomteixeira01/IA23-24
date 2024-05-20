# Auxiliary functions

from connections import *

def all_connections_valid() -> bool:
    """ funcao que vai verificar se as coneccoes sao válidas """
    # Deve levar em conta a orientação das peças e a presença de vizinhos adequados.
    pass

def get_possible_movements(row: int, col: int, piece: str):
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
        
        elif col == 1:
            if p == 'F': possibilities.extend(['FE', 'FD', 'FB'])
            if p == 'B': possibilities.append('BB')
            if p == 'V': possibilities.extend(['VB', 'VE'])
            if p == 'L': possibilities.append('LH')
        
        elif col == 2:
            if p == 'F': possibilities.extend(['FE', 'FB'])
            if p == 'B': None
            if p == 'V': possibilities.append('VE')
            if p == 'L': None
        
        else:
            # outside of board
            pass

    if row == 1:
        
        if col == 0:
            if p == 'F': possibilities.extend(['FC', 'FD', 'FB'])
            if p == 'B': possibilities.append('BD')
            if p == 'V': possibilities.extend(['VD', 'VB'])
            if p == 'L': possibilities.append('LV')
        
        elif col == 1:
            if p == 'F': possibilities.extend(['FE', 'FC', 'FD', 'FB'])
            if p == 'B': possibilities.extend(['BE', 'BC', 'BD', 'BB'])
            if p == 'V': possibilities.extend(['VE', 'VC', 'VD', 'VB'])
            if p == 'L': possibilities.extend(['LH', 'LV'])
        
        elif col == 2:
            if p == 'F': possibilities.extend(['FE', 'FB', 'FC'])
            if p == 'B': possibilities.append('BE')
            if p == 'V': possibilities.extend(['VC', 'VE'])
            if p == 'L': possibilities.append('LV')
        
        else:
            # outside of board
            pass

    if row == 2:
        
        if col == 0:
            if p == 'F': possibilities.extend(['FC', 'FD'])
            if p == 'B': None
            if p == 'V': possibilities.append('VD')
            if p == 'L': None
        
        elif col == 1:
            if p == 'F': possibilities.extend(['FE', 'FC', 'FD'])
            if p == 'B': possibilities.append('BC')
            if p == 'V': possibilities.extend(['VC', 'VD'])
            if p == 'L': possibilities.append('LH')
        
        elif col == 2:
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

    # cantos (0,0) (0,2) (2,0) (2,2)
    if row == 0 and col == 0:
        # vizinho -> direita e baixo
        return [(board[0][1], (0,1)), (board[1][0], (1,0))]
    
    if row == 0 and col == 2:
        # vizinho -> esquerda e baixo
        return [(board[0][1], (0,1)), (board[1,2], (1,2))]
    
    if row == 2 and col == 0:
        # vizinhos -> cima e direita
        return [(board[1][0], (1,0)), (board[2][1], (2,1))]
    
    if row == 2 and col == 2:
        # vizinhos -> cima e esquerda
        return [(board[1][2], (1,2)), (board[2][1], (2,1))]

    # paredes (0,1) (1,0) (1,2) (2,1)
    if row == 0 and col == 1:
        # vizinhos -> esquerda, direita, baixo
        return [(board[0][0], (0,0)), 
                (board[0][2], (0,2)), 
                (board[1][1], (1,1))]

    if row == 1 and col == 0:
        # vizinhos -> cima, direita, baixo
        return [(board[0][0], (0,0)), 
                (board[1][1], (1,1)), 
                (board[2][0], (2,0))]
    
    if row == 1 and col == 2:
        # vizinhos -> cima, baixo, esquerda
        return [(board[0][2], (0,2)), 
                (board[2][2], (2,2)), 
                (board[1][1], (1,1))]
    
    if row == 2 and col == 1:
        # vizinhos -> esquerda, cima, direita
        return [(board[2][0], (2,0)), 
                (board[1][1], (1,1)), 
                (board[2][2], (2,2))]

    # meio (1,1)
    else:
        # vizinhos -> esquerda, cima, direita, baixo
        return [(board[row][col-1], (row,col-1)), 
                (board[row-1][col], (row-1,col)), 
                (board[row][col+1], (row,col+1)), 
                (board[row+1][col], (row+1,col))]


def can_connect(piece1, pos1, piece2, pos2):
    """ Verfica se duas pecas conectam 
    Retorna True se a conecção for válida, False caso contrário"""

    p1_type, p1_orientation = piece1[0], piece1[1]
    p2_type, p2_orientation = piece2[0], piece2[1]

    # Acessar as conexões possíveis para a primeira peça na sua posição
    p1_connections = connections.get(pos1, {})
    if not p1_connections:
        return False  # Não há conexões definidas para a primeira peça na posição pos1

    # Dentro das conexões da primeira peça, buscar a configuração específica pela orientação
    p1_orient_connections = p1_connections.get(p1_type + p1_orientation, {})
    if not p1_orient_connections:
        return False  # Não há conexões definidas para a orientação específica da primeira peça

    # Para cada posição e orientação possível de conexão da primeira peça,
    # verifica se a segunda peça e sua orientação estão listadas como uma conexão válida
    for connection_pos, valid_connections in p1_orient_connections.items():
        if connection_pos == pos2:
            # Verifica se a segunda peça com sua orientação está entre as conexões válidas
            if p2_type + p2_orientation in valid_connections:
                return True

    return False


def count_valid_connections(board):
    total_connections = 0
    for row in range(len(board.board)):
        for col in range(len(board.board[0])):
            total_connections += count_connections(board, row, col)
    return total_connections

