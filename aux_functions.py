# Auxiliary functions

def all_connections_valid() -> bool:
    """ funcao que vai verificar se as coneccoes sao válidas """
    pass

def get_possible_movements(row: int, col: int, piece: str):
    """ funcao que vai retornar todos os possiveis movimentos de uma dada peca num dada posicao
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
