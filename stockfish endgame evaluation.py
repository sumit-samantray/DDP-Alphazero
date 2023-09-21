def end_game_evaluation(pos, nowinnable):
    v = 0
    v += piece_value_eg(pos) - piece_value_eg(colorflip(pos))
    v += psqt_eg(pos) - psqt_eg(colorflip(pos))
    v += imbalance_total(pos)
    v += pawns_eg(pos) - pawns_eg(colorflip(pos))
    v += pieces_eg(pos) - pieces_eg(colorflip(pos))
    v += mobility_eg(pos) - mobility_eg(colorflip(pos))
    v += threats_eg(pos) - threats_eg(colorflip(pos))
    v += passed_eg(pos) - passed_eg(colorflip(pos))
    v += king_eg(pos) - king_eg(colorflip(pos))
    if not nowinnable:
        v += winnable_total_eg(pos, v)
    return v

def piece_value_eg(pos, square=None):
    if square is None:
        return sum(pos, piece_value_eg)
    return piece_value_bonus(pos, square, False)

def piece_value_bonus(pos, square, mg):
    if square is None:
        return sum(pos, piece_value_bonus)
    a = [124, 781, 825, 1276, 2538] if mg else [206, 854, 915, 1380, 2682]
    i = "PNBRQ".index(board(pos, square.x, square.y))
    if i >= 0:
        return a[i]
    return 0

def psqt_eg(pos, square=None):
    if square is None:
        return sum(pos, psqt_eg)
    return psqt_bonus(pos, square, False)

def psqt_bonus(pos, square, mg):
    if square is None:
        return sum(pos, psqt_bonus, mg)
    bonus = [
        [[-175, -92, -74, -73], [-77, -41, -27, -15], [-61, -17, 6, 12], [-35, 8, 40, 49], [-34, 13, 44, 51], [-9, 22, 58, 53], [-67, -27, 4, 37], [-201, -83, -56, -26]],
        [[-53, -5, -8, -23], [-15, 8, 19, 4], [-7, 21, -5, 17], [-5, 11, 25, 39], [-12, 29, 22, 31], [-16, 6, 1, 11], [-17, -14, 5, 0], [-48, 1, -14, -23]],
        [[-31, -20, -14, -5], [-21, -13, -8, 6], [-25, -11, -1, 3], [-13, -5, -4, -6], [-27, -15, -4, 3], [-22, -2, 6, 12], [-2, 12, 16, 18], [-17, -19, -1, 9]],
        [[3, -5, -5, 4], [-3, 5, 8, 12], [-3, 6, 13, 7], [4, 5, 9, 8], [0, 14, 12, 5], [-4, 10, 6, 8], [-5, 6, 10, 8], [-2, -2, 1, -2]],
        [[271, 327, 271, 198], [278, 303, 234, 179], [195, 258, 169, 120], [164, 190, 138, 98], [154, 179, 105, 70], [123, 145, 81, 31], [88, 120, 65, 33], [59, 89, 45, -1]]
    ] if mg else [
        [[-96, -65, -49, -21], [-67, -54, -18, 8], [-40, -27, -8, 29], [-35, -2, 13, 28], [-45, -16, 9, 39], [-51, -44, -16, 17], [-69, -50, -51, 12], [-100, -88, -56, -17]],
        [[-57, -30, -37, -12], [-37, -13, -17, 1], [-16, -1, -2, 10], [-20, -6, 0, 17], [-17, -1, -14, 15], [-30, 6, 4, 6], [-31, -20, -1, 1], [-46, -42, -37, -24]],
        [[-9, -13, -16, -7], [-10, -6, -3, 6], [-8, -5, 1, 8], [-5, 0, 5, 7], [-8, -3, 4, 6], [-8, -1, 6, 10], [0, 0, 8, 9], [-9, -5, -2, 1]],
        [[-13, -11, -3, 5], [-5, -4, 3, 9], [-8, 2, 10, 12], [-6, 3, 12, 18], [-11, 1, 14, 22], [-10, -3, 10, 16], [-13, -6, 10, 13], [-10, -9, 3, 0]],
        [[-140, -115, -97, -73], [-120, -101, -74, -53], [-78, -50, -27, -6], [-53, -30, -9, 10], [-55, -31, -13, 5], [-58, -33, -13, 5], [-59, -33, -14, 1], [-94, -76, -56, -36]]
    ]
    i = "PNBRQ".index(board(pos, square.x, square.y))
    return bonus[i][square.x][square.y]

def imbalance_total(pos):
    mg = 0
    eg = 0
    mgpawns = 0
    egpawns = 0
    mgminors = 0
    egminors = 0
    mgmobility = 0
    egmobility = 0
    mgattacks = 0
    egattacks = 0
    egkingattacks = 0
    mgkingattacks = 0
    piece_types = "PNBRQ"
    for x in range(8):
        for y in range(8):
            piece = board(pos, x, y)
            if piece == ' ':
                continue
            i = piece_types.index(piece)
            mg += piece_value_bonus(pos, Square(x, y), True)
            eg += piece_value_bonus(pos, Square(x, y), False)
            if i == 0:
                mgpawns += 1
            elif i == 3 or i == 2:
                mgminors += 1
            elif i == 4:
                mgmobility += 1
            mgattacks += len(attacks(pos, x, y, True))
            egattacks += len(attacks(pos, x, y, False))
            if (attacks(pos, x, y, False) and piece == 'K') or (attacks(pos, x, y, True) and piece == 'k'):
                mgkingattacks += 1
            elif (attacks(pos, x, y, False) and piece == 'k') or (attacks(pos, x, y, True) and piece == 'K'):
                egkingattacks += 1
    eg += egmobility * 15
    mg += mgmobility * 15
    return mg - eg

def pawns_eg(pos):
    return pawn_structure_eg(pos) + pawn_king_safety_eg(pos) + pawn_passed_eg(pos) + pawn_storm_eg(pos) + pawn_king_distance_eg(pos)

def pawn_structure_eg(pos):
    pawns = {True: [], False: []}
    isolated_pawn_penalty = [-20, -14, -7, -3, -3, -7, -14, -20]
    backwards_pawn_penalty = [-10, -4, 0, 0, 0, 0, -4, -10]
    doubled_pawn_penalty = [-12, -8, -4, -2, -2, -4, -8, -12]

    for x in range(8):
        for y in range(8):
            piece = board(pos, x, y)
            if piece == 'P':
                pawns[True].append(Square(x, y))
            elif piece == 'p':
                pawns[False].append(Square(x, y))

    pawn_score = 0

    for color in [True, False]:
        for square in pawns[color]:
            x, y = square.x, square.y
            if color:
                is_isolated = not any(
                    board(pos, x - 1, y - 1) == 'P' or board(pos, x + 1, y - 1) == 'P' for y in range(2, 8))
                is_doubled = any(board(pos, x, y - 1) == 'P' for y in range(1, 8))
                is_backwards = not any(
                    board(pos, x - 1, y - 1) == 'P' or board(pos, x + 1, y - 1) == 'P' for y in range(y + 1, 8))
                if is_isolated:
                    pawn_score += isolated_pawn_penalty[y]
                if is_doubled:
                    pawn_score += doubled_pawn_penalty[y]
                if is_backwards:
                    pawn_score += backwards_pawn_penalty[y]
            else:
                is_isolated = not any(
                    board(pos, x - 1, y + 1) == 'p' or board(pos, x + 1, y + 1) == 'p' for y in range(0, 6))
                is_doubled = any(board(pos, x, y + 1) == 'p' for y in range(0, 7))
                is_backwards = not any(
                    board(pos, x - 1, y + 1) == 'p' or board(pos, x + 1, y + 1) == 'p' for y in range(0, y))
                if is_isolated:
                    pawn_score += isolated_pawn_penalty[y]
                if is_doubled:
                    pawn_score += doubled_pawn_penalty[y]
                if is_backwards:
                    pawn_score += backwards_pawn_penalty[y]

    return pawn_score

def pawn_king_safety_eg(pos):
    safety = 0
    for x in range(8):
        for y in range(8):
            if board(pos, x, y) == 'K':
                safety += len(attacks(pos, x, y, True))
            elif board(pos, x, y) == 'k':
                safety -= len(attacks(pos, x, y, False))
    return safety * 3

def pawn_passed_eg(pos):
    passed_pawn_bonus = [0, 5, 10, 20, 35, 65, 120, 200, 350, 600]
    passed_pawn_score = 0
    for x in range(8):
        for y in range(8):
            if board(pos, x, y) == 'P':
                passed_pawn_score += passed_pawn_bonus[y]
            elif board(pos, x, y) == 'p':
                passed_pawn_score -= passed_pawn_bonus[7 - y]
    return passed_pawn_score

def pawn_storm_eg(pos):
    storm = 0
    for x in range(8):
        for y in range(4, 8):
            if board(pos, x, y) == 'P':
                storm += 1
            elif board(pos, x, y) == 'p':
                storm -= 1
    return storm * 5

def pawn_king_distance_eg(pos):
    distance_score = 0
    for x in range(8):
        for y in range(8):
            if board(pos, x, y) == 'P':
                distance_score += y
            elif board(pos, x, y) == 'p':
                distance_score -= 7 - y
    return distance_score * 4

def eval_eg(pos):
    mg = material_eg(pos) + pawns_eg(pos) + knight_eg(pos) + bishop_eg(pos) + rook_eg(pos) + queen_eg(pos)
    eg = pawn_structure_eg(pos) + pawn_king_safety_eg(pos) + pawn_passed_eg(pos) + pawn_storm_eg(pos) + pawn_king_distance_eg(
        pos) + knight_eg(pos) + bishop_eg(pos) + rook_eg(pos) + queen_eg(pos)
    return mg, eg

def evaluation_eg(pos):
    mg, eg = eval_eg(pos)
    if board_color_eg(pos):
        return mg, eg
    return eg, mg

def search(pos, depth, alpha, beta, maximizing):
    if depth == 0 or is_draw(pos) or is_checkmate(pos) or is_stalemate(pos):
        return evaluation_eg(pos)

    moves = []
    for move in generate_legal_moves(pos):
        make_move(pos, move)
        moves.append(move)
        unmake_move(pos, move)

    if maximizing:
        max_eval = float('-inf')
        for move in moves:
            make_move(pos, move)
            eval = search(pos, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval[0])
            alpha = max(alpha, eval[0])
            unmake_move(pos, move)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            make_move(pos, move)
            eval = search(pos, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval[1])
            beta = min(beta, eval[1])
            unmake_move(pos, move)
            if beta <= alpha:
                break
        return min_eval

def best_move_eg(pos, depth):
    best_move = None
    max_eval = float('-inf')
    moves = []
    for move in generate_legal_moves(pos):
        make_move(pos, move)
        moves.append(move)
        unmake_move(pos, move)
    for move in moves:
        make_move(pos, move)
        eval = search(pos, depth - 1, float('-inf'), float('inf'), False)
        if eval > max_eval:
            max_eval = eval
            best_move = move
        unmake_move(pos, move)
    return best_move

def negamax(pos, depth, alpha, beta, color):
    if depth == 0 or is_draw(pos) or is_checkmate(pos) or is_stalemate(pos):
        return color * evaluation_eg(pos)

    max_eval = float('-inf')
    for move in generate_legal_moves(pos):
        make_move(pos, move)
        eval = -negamax(pos, depth - 1, -beta, -alpha, -color)
        max_eval = max(max_eval, eval)
        alpha = max(alpha, eval)
        unmake_move(pos, move)
        if beta <= alpha:
            break
    return max_eval

def best_move_negamax(pos, depth):
    best_move = None
    max_eval = float('-inf')
    moves = []
    for move in generate_legal_moves(pos):
        make_move(pos, move)
        moves.append(move)
        unmake_move(pos, move)
    for move in moves:
        make_move(pos, move)
        eval = -negamax(pos, depth - 1, float('-inf'), float('inf'), -1)
        if eval > max_eval:
            max_eval = eval
            best_move = move
        unmake_move(pos, move)
    return best_move

def make_move(pos, move):
    from_x, from_y, to_x, to_y = move
    pos[to_x][to_y] = pos[from_x][from_y]
    pos[from_x][from_y] = ' '

def unmake_move(pos, move):
    from_x, from_y, to_x, to_y = move
    pos[from_x][from_y] = pos[to_x][to_y]
    pos[to_x][to_y] = move[4]

def generate_moves(pos):
    moves = []
    for from_x in range(8):
        for from_y in range(8):
            if board_color_eg(pos):
                piece = pos[from_x][from_y]
            else:
                piece = pos[7 - from_x][7 - from_y]
            if not piece.isspace():
                for to_x in range(8):
                    for to_y in range(8):
                        move = (from_x, from_y, to_x, to_y)
                        if is_legal_move(pos, move):
                            moves.append(move)
    return moves

def is_draw(pos):
    return pos in draw_positions

def is_checkmate(pos):
    return is_in_check(pos) and not any(is_legal_move(pos, move) for move in generate_moves(pos))

def is_stalemate(pos):
    return not is_in_check(pos) and not any(is_legal_move(pos, move) for move in generate_moves(pos))

def is_in_check(pos):
    if board_color_eg(pos):
        color = 'w'
    else:
        color = 'b'
    king_x, king_y = find_king(pos, color)
    for from_x in range(8):
        for from_y in range(8):
            if board_color_eg(pos):
                piece = pos[from_x][from_y]
            else:
                piece = pos[7 - from_x][7 - from_y]
            if not piece.isspace() and piece.islower() if color == 'w' else piece.isupper():
                for to_x in range(8):
                    for to_y in range(8):
                        move = (from_x, from_y, to_x, to_y)
                        if is_legal_move(pos, move):
                            if to_x == king_x and to_y == king_y:
                                return True
    return False

def find_king(pos, color):
    for x in range(8):
        for y in range(8):
            if pos[x][y] == ('K' if color == 'w' else 'k'):
                return x, y

def is_legal_move(pos, move):
    from_x, from_y, to_x, to_y = move
    piece = pos[from_x][from_y]
    if piece == ' ':
        return False
    if board_color_eg(pos):
        color = 'w' if piece.isupper() else 'b'
    else:
        color = 'b' if piece.isupper() else 'w'
    if (color == 'w' and not piece.isupper()) or (color == 'b' and not piece.islower()):
        return False
    if piece.upper() == 'P':
        return is_pawn_legal(pos, move)
    elif piece.upper() == 'R':
        return is_rook_legal(pos, move)
    elif piece.upper() == 'N':
        return is_knight_legal(pos, move)
    elif piece.upper() == 'B':
        return is_bishop_legal(pos, move)
    elif piece.upper() == 'Q':
        return is_queen_legal(pos, move)
    elif piece.upper() == 'K':
        return is_king_legal(pos, move)
    return False

def is_pawn_legal(pos, move):
    from_x, from_y, to_x, to_y = move
    piece = pos[from_x][from_y]
    if piece.isupper():
        direction = -1
        starting_rank = 6
        en_passant_rank = 3
    else:
        direction = 1
        starting_rank = 1
        en_passant_rank = 4
    if from_x == to_x:
        if from_y + direction == to_y and pos[to_x][to_y] == ' ':
            return True
        if from_y + 2 * direction == to_y and from_x == starting_rank and pos[to_x][to_y] == ' ' and pos[from_x + direction][to_y] == ' ':
            return True
    elif abs(to_x - from_x) == 1 and from_y + direction == to_y:
        if to_x == en_passant_rank and pos[to_x - direction][to_y] == ('P' if piece.isupper() else 'p'):
            return True
        if pos[to_x][to_y].islower() if piece.isupper() else pos[to_x][to_y].isupper():
            return True
    return False

def is_rook_legal(pos, move):
    from_x, from_y, to_x, to_y = move
    if from_x != to_x and from_y != to_y:
        return False
    if from_x == to_x:
        for y in range(min(from_y, to_y) + 1, max(from_y, to_y)):
            if pos[from_x][y] != ' ':
                return False
    else:
        for x in range(min(from_x, to_x) + 1, max(from_x, to_x)):
            if pos[x][from_y] != ' ':
                return False
    return True

def is_knight_legal(pos, move):
    from_x, from_y, to_x, to_y = move
    dx = abs(to_x - from_x)
    dy = abs(to_y - from_y)
    return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)

def is_bishop_legal(pos, move):
    from_x, from_y, to_x, to_y = move
    if abs(to_x - from_x) != abs(to_y - from_y):
        return False
    dx = 1 if from_x < to_x else -1
    dy = 1 if from_y < to_y else -1
    x, y = from_x + dx, from_y + dy
    while x != to_x:
        if pos[x][y] != ' ':
            return False
        x += dx
        y += dy
    return True

def is_queen_legal(pos, move):
    from_x, from_y, to_x, to_y = move
    if from_x == to_x or from_y == to_y:
        return is_rook_legal(pos, move)
    if abs(to_x - from_x) == abs(to_y - from_y):
        return is_bishop_legal(pos, move)
    return False

def is_king_legal(pos, move):
    from_x, from_y, to_x, to_y = move
    dx = abs(to_x - from_x)
    dy = abs(to_y - from_y)
    return dx <= 1 and dy <= 1

def board_color_eg(pos):
    return sum(sum(piece.isupper() for piece in row) for row in pos) > 32

def attacks(pos, x, y, mg):
    attacks = []
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
    for dx, dy in directions:
        for i in range(1, 8):
            to_x, to_y = x + i * dx, y + i * dy
            if not (0 <= to_x < 8 and 0 <= to_y < 8):
                break
            to_piece = board(pos, to_x, to_y)
            if to_piece != ' ':
                if mg:
                    if to_piece.isupper():
                        attacks.append((to_x, to_y))
                else:
                    if to_piece.islower():
                        attacks.append((to_x, to_y))
                break
    return attacks

def passed_eg(pos, square=None):
    if square is None:
        return sum(pos, passed_eg)
    return passed_bonus(pos, square, False)

def passed_bonus(pos, square, mg):
    if square is None:
        return sum(pos, passed_bonus, mg)
    bonus = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [-2, -4, 0, 0, 0, 0, -4, -2],
        [-3, -6, -9, 0, 0, -9, -6, -3],
        [-4, -8, -12, -16, -16, -12, -8, -4],
        [-4, -8, -12, -16, -16, -12, -8, -4],
        [-3, -6, -9, -12, -12, -9, -6, -3],
        [-2, -4, -6, 0, 0, -6, -4, -2],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ] if mg else [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [2, 4, 0, 0, 0, 0, 4, 2],
        [3, 6, 9, 0, 0, 9, 6, 3],
        [4, 8, 12, 16, 16, 12, 8, 4],
        [4, 8, 12, 16, 16, 12, 8, 4],
        [3, 6, 9, 12, 12, 9, 6, 3],
        [2, 4, 6, 0, 0, 6, 4, 2],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]
    i = "PNBRQ".index(board(pos, square.x, square.y))
    return bonus[i][square.x][square.y]

def imbalance_total(pos):
    mg = 0
    eg = 0
    mgpawns = 0
    egpawns = 0
    mgminors = 0
    egminors = 0
    mgmobility = 0
    egmobility = 0
    mgattacks = 0
    egattacks = 0
    egkingattacks = 0
    mgkingattacks = 0
    piece_types = "PNBRQ"
    for x in range(8):
        for y in range(8):
            piece = board(pos, x, y)
            if piece == ' ':
                continue
            i = piece_types.index(piece)
            mg += piece_value_bonus(pos, Square(x, y), True)
            eg += piece_value_bonus(pos, Square(x, y), False)
            if i == 0:
                mgpawns += 1
            elif i == 3 or i == 2:
                mgminors += 1
            elif i == 4:
                mgmobility += 1
            mgattacks += len(attacks(pos, x, y, True))
            egattacks += len(attacks(pos, x, y, False))
            if (attacks(pos, x, y, False) and piece == 'K') or (attacks(pos, x, y, True) and piece == 'k'):
                mgkingattacks += 1
            elif (attacks(pos, x, y, False) and piece == 'k') or (attacks(pos, x, y, True) and piece == 'K'):
                egkingattacks += 1
    eg += egmobility * 15
    mg += mgmobility * 15
    return mg - eg

def pawns_eg(pos):
    return pawn_structure_eg(pos) + pawn_king_safety_eg(pos) + pawn_passed_eg(pos) + pawn_storm_eg(pos) + pawn_king_distance_eg(pos)

def pawn_structure_eg(pos):
    pawns = {True: [], False: []}
    isolated_pawn_penalty = [-20, -14, -7, -3, -3, -7, -14, -20]
    backwards_pawn_penalty = [-10, -4, 0, 0, 0, 0, -4, -10]
    doubled_pawn_penalty = [-12, -8, -4, -2, -2, -4, -8, -12]

    for x in range(8):
        for y in range(8):
            piece = board(pos, x, y)
            if piece == 'P':
                pawns[True].append(Square(x, y))
            elif piece == 'p':
                pawns[False].append(Square(x, y))

    pawn_score = 0

    for color in [True, False]:
        for square in pawns[color]:
            x, y = square.x, square.y
            if color:
                is_isolated = not any(
                    board(pos, x - 1, y - 1) == 'P' or board(pos, x + 1, y - 1) == 'P' for y in range(2, 8))
                is_doubled = any(board(pos, x, y - 1) == 'P' for y in range(1, 8))
                is_backwards = not any(
                    board(pos, x - 1, y - 1) == 'P' or board(pos, x + 1, y - 1) == 'P' for y in range(y + 1, 8))
                if is_isolated:
                    pawn_score += isolated_pawn_penalty[y]
                if is_doubled:
                    pawn_score += doubled_pawn_penalty[y]
                if is_backwards:
                    pawn_score += backwards_pawn_penalty[y]
            else:
                is_isolated = not any(
                    board(pos, x - 1, y + 1) == 'p' or board(pos, x + 1, y + 1) == 'p' for y in range(0, 6))
                is_doubled = any(board(pos, x, y + 1) == 'p' for y in range(0, 7))
                is_backwards = not any(
                    board(pos, x - 1, y + 1) == 'p' or board(pos, x + 1, y + 1) == 'p' for y in range(0, y))
                if is_isolated:
                    pawn_score += isolated_pawn_penalty[y]
                if is_doubled:
                    pawn_score += doubled_pawn_penalty[y]
                if is_backwards:
                    pawn_score += backwards_pawn_penalty[y]

    return pawn_score

def pawn_king_safety_eg(pos):
    safety = 0
    for x in range(8):
        for y in range(8):
            if board(pos, x, y) == 'K':
                safety += len(attacks(pos, x, y, True))
            elif board(pos, x, y) == 'k':
                safety -= len(attacks(pos, x, y, False))
    return safety * 3

def pawn_passed_eg(pos):
    passed_pawn_bonus = [0, 5, 10, 20, 35, 65, 120, 200, 350, 600]
    passed_pawn_score = 0
    for x in range(8):
        for y in range(8):
            if board(pos, x, y) == 'P':
                passed_pawn_score += passed_pawn_bonus[y]
            elif board(pos, x, y) == 'p':
                passed_pawn_score -= passed_pawn_bonus[7 - y]
    return passed_pawn_score

def pawn_storm_eg(pos):
    storm = 0
    for x in range(8):
        for y in range(4, 8):
            if board(pos, x, y) == 'P':
                storm += 1
            elif board(pos, x, y) == 'p':
                storm -= 1
    return storm * 5

def pawn_king_distance_eg(pos):
    distance_score = 0
    for x in range(8):
        for y in range(8):
            if board(pos, x, y) == 'P':
                distance_score += y
            elif board(pos, x, y) == 'p':
                distance_score -= 7 - y
    return distance_score * 4

def eval_eg(pos):
    mg = material_eg(pos) + pawns_eg(pos) + knight_eg(pos) + bishop_eg(pos) + rook_eg(pos) + queen_eg(pos)
    eg = pawn_structure_eg(pos) + pawn_king_safety_eg(pos) + pawn_passed_eg(pos) + pawn_storm_eg(pos) + pawn_king_distance_eg(
        pos) + knight_eg(pos) + bishop_eg(pos) + rook_eg(pos) + queen_eg(pos)
    return mg, eg

def evaluation_eg(pos):
    mg, eg = eval_eg(pos)
    if board_color_eg(pos):
        return mg, eg
    return eg, mg

def search(pos, depth, alpha, beta, maximizing):
    if depth == 0 or is_draw(pos) or is_checkmate(pos) or is_stalemate(pos):
        return evaluation_eg(pos)

    moves = []
    for move in generate_legal_moves(pos):
        make_move(pos, move)
        moves.append(move)
        unmake_move(pos, move)

    if maximizing:
        max_eval = float('-inf')
        for move in moves:
            make_move(pos, move)
            eval = search(pos, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval[0])
            alpha = max(alpha, eval[0])
            unmake_move(pos, move)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            make_move(pos, move)
            eval = search(pos, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval[1])
            beta = min(beta, eval[1])
            unmake_move(pos, move)
            if beta <= alpha:
                break
        return min_eval

def best_move_eg(pos, depth):
    best_move = None
    max_eval = float('-inf')
    moves = []
    for move in generate_legal_moves(pos):
        make_move(pos, move)
        moves.append(move)
        unmake_move(pos, move)
    for move in moves:
        make_move(pos, move)
        eval = search(pos, depth - 1, float('-inf'), float('inf'), False)
        if eval > max_eval:
            max_eval = eval
            best_move = move
        unmake_move(pos, move)
    return best_move

def pawns_eg(pos):
    return pawn_structure_eg(pos) + pawn_king_safety_eg(pos) + pawn_passed_eg(pos) + pawn_storm_eg(pos) + pawn_king_distance_eg(pos)

def pawn_structure_eg(pos):
    pawns = {True: [], False: []}
    isolated_pawn_penalty = [-20, -14, -7, -3, -3, -7, -14, -20]
    backwards_pawn_penalty = [-10, -4, 0, 0, 0, 0, -4, -10]
    doubled_pawn_penalty = [-12, -8, -4, -2, -2, -4, -8, -12]

    for x in range(8):
        for y in range(8):
            piece = board(pos, x, y)
            if piece == 'P':
                pawns[True].append(Square(x, y))
            elif piece == 'p':
                pawns[False].append(Square(x, y))

    pawn_score = 0

    for color in [True, False]:
        for square in pawns[color]:
            x, y = square.x, square.y
            if color:
                is_isolated = not any(
                    board(pos, x - 1, y - 1) == 'P' or board(pos, x + 1, y - 1) == 'P' for y in range(2, 8))
                is_doubled = any(board(pos, x, y - 1) == 'P' for y in range(1, 8))
                is_backwards = not any(
                    board(pos, x - 1, y - 1) == 'P' or board(pos, x + 1, y - 1) == 'P' for y in range(y + 1, 8))
                if is_isolated:
                    pawn_score += isolated_pawn_penalty[y]
                if is_doubled:
                    pawn_score += doubled_pawn_penalty[y]
                if is_backwards:
                    pawn_score += backwards_pawn_penalty[y]
            else:
                is_isolated = not any(
                    board(pos, x - 1, y + 1) == 'p' or board(pos, x + 1, y + 1) == 'p' for y in range(0, 6))
                is_doubled = any(board(pos, x, y + 1) == 'p' for y in range(0, 7))
                is_backwards = not any(
                    board(pos, x - 1, y + 1) == 'p' or board(pos, x + 1, y + 1) == 'p' for y in range(0, y))
                if is_isolated:
                    pawn_score += isolated_pawn_penalty[y]
                if is_doubled:
                    pawn_score += doubled_pawn_penalty[y]
                if is_backwards:
                    pawn_score += backwards_pawn_penalty[y]

    return pawn_score

def pawn_king_safety_eg(pos):
    safety = 0
    for x in range(8):
        for y in range(8):
            if board(pos, x, y) == 'K':
                safety += len(attacks(pos, x, y, True))
            elif board(pos, x, y) == 'k':
                safety -= len(attacks(pos, x, y, False))
    return safety * 3

def pawn_passed_eg(pos):
    passed_pawn_bonus = [0, 5, 10, 20, 35, 65, 120, 200, 350, 600]
    passed_pawn_score = 0
    for x in range(8):
        for y in range(8):
            if board(pos, x, y) == 'P':
                passed_pawn_score += passed_pawn_bonus[y]
            elif board(pos, x, y) == 'p':
                passed_pawn_score -= passed_pawn_bonus[7 - y]
    return passed_pawn_score

def pawn_storm_eg(pos):
    storm = 0
    for x in range(8):
        for y in range(4, 8):
            if board(pos, x, y) == 'P':
                storm += 1
            elif board(pos, x, y) == 'p':
                storm -= 1
    return storm * 5
