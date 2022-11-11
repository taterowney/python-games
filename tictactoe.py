import copy

COMPUTER = True
PLAYER = False

PLAYER_SHAPE = 'X'
COMPUTER_SHAPE = 'O'

shapes = {COMPUTER: COMPUTER_SHAPE, PLAYER: PLAYER_SHAPE}

DRAW = 'draw'

def game(starting_player=PLAYER):
    board = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
    if starting_player == COMPUTER:
        board, _ = best_move(board)
    while 1:
        board, win = get_player_input(board)
        if win == PLAYER_SHAPE:
            print("Player wins!")
            return
        elif win == DRAW:
            print("Tie!")
            return
#        time.sleep(1)
        board, win = best_move(board)
        if win == COMPUTER_SHAPE:
            print("Player loses...")
            return
        elif win == DRAW:
            print("Tie!")
            return

def minimax(board, turn = COMPUTER,depth = 0):
    outcomes = [[None, None, None], [None, None, None], [None, None, None]]
    if detect_win(board) == PLAYER_SHAPE:
        return (-10, None, None)
    elif detect_win(board) == COMPUTER_SHAPE:
        return (10, None, None)
    elif detect_win(board) == DRAW:
        return (0, None, None)
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == '_':
                new_board = copy.deepcopy(board)
                new_board[i][j] = shapes[turn]
#                print(minimax(new_board, turn=not turn))
                outcomes[i][j] = minimax(new_board, turn=not turn, depth=depth+1)[0]
    if depth == 0:
        print()
    if turn == PLAYER:
        minval = 1000
        for i in range(len(outcomes)):
            for j in range(len(outcomes[i])):
                if outcomes[i][j] == None:
                    outcomes[i][j] = 1000
                elif minval > outcomes[i][j]:
                    minval = outcomes[i][j]
                    vert = i
                    horiz = j
#        vert = outcomes.index(min(outcomes))
#       horiz = outcomes[vert].index(min(outcomes[vert]))
        return (outcomes[vert][horiz]+depth, vert, horiz)
    elif turn == COMPUTER:
        maxval = -1000
        for i in range(len(outcomes)):
            for j in range(len(outcomes[i])):
                if outcomes[i][j] == None:
                    outcomes[i][j] = -1000
                elif maxval < outcomes[i][j]:
                    maxval = outcomes[i][j]
                    vert = i
                    horiz = j
#        vert = outcomes.index(max(outcomes))
#        horiz = outcomes[vert].index(max(outcomes[vert]))
        return (outcomes[vert][horiz]-depth, vert, horiz)

def best_move(board):
    coords = minimax(board)
    horiz = coords[2]
    vert = coords[1]
    board[vert][horiz] = COMPUTER_SHAPE
    return board, detect_win(board)

def get_player_input(board):
    print_board(board)
    move = input().lower().split(' ')
    move_horiz = 1
    move_vert = 1
    if 'left' in move:
        move_horiz = 0
    elif 'right' in move:
        move_horiz = 2
    if 'upper' in move or 'top' in move:
        move_vert = 0
    elif 'lower' in move or 'bottom' in move:
        move_vert = 2
    if board[move_vert][move_horiz] == '_':
        board[move_vert][move_horiz] = PLAYER_SHAPE
        print_board(board)
        return board, detect_win(board)
    else:
        print()
        print("That space is already occupied!")
        print()
        return get_player_input(board)

def detect_win(board):
    for row in board:
        if row[0] == row[1] and row[1] == row[2] and row[0] != '_':
            return row[0]
    for i in range(3):
        if board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] != '_':
            return board[0][i]
    if board[0][0] == board[1][1] and board[2][2] == board[1][1] and board[0][0] != '_':
        return board[0][0]
    if board[2][0] == board[1][1] and board[0][2] == board[1][1] and board[2][0] != '_':
        return board[2][0]
    for i in range(len(board)):
        for j in board[i]:
            if j == '_':
                return None
    return DRAW

def print_board(board):
    for i in range(len(board)):
        printval = ''
        for j in range(len(board[i])):
            printval += board[i][j]
            printval += ' '
        print(printval)

if __name__ == '__main__':
    game()
