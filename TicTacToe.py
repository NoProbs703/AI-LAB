board = {
    1: ' ', 2: ' ', 3: ' ',
    4: ' ', 5: ' ', 6: ' ',
    7: ' ', 8: ' ', 9: ' '
}

def printBoard(board):
    print(board[1] + '|' + board[2] + '|' + board[3])
    print('-+-+-')
    print(board[4] + '|' + board[5] + '|' + board[6])
    print('-+-+-')
    print(board[7] + '|' + board[8] + '|' + board[9])
    print('\n')

def spaceFree(pos):
    if board[pos] == ' ':
        return True
    else:
        return False

def checkWin():
    if board[1] == board[2] == board[3] != ' ':
        return True
    elif board[4] == board[5] == board[6] != ' ':
        return True
    elif board[7] == board[8] == board[9] != ' ':
        return True
    elif board[1] == board[5] == board[9] != ' ':
        return True
    elif board[3] == board[5] == board[7] != ' ':
        return True
    elif board[1] == board[4] == board[7] != ' ':
        return True
    elif board[2] == board[5] == board[8] != ' ':
        return True
    elif board[3] == board[6] == board[9] != ' ':
        return True
    else:
        return False

def checkMoveForWin(move):
    if board[1] == board[2] == board[3] == move:
        return True
    elif board[4] == board[5] == board[6] == move:
        return True
    elif board[7] == board[8] == board[9] == move:
        return True
    elif board[1] == board[5] == board[9] == move:
        return True
    elif board[3] == board[5] == board[7] == move:
        return True
    elif board[1] == board[4] == board[7] == move:
        return True
    elif board[2] == board[5] == board[8] == move:
        return True
    elif board[3] == board[6] == board[9] == move:
        return True
    else:
        return False

def checkDraw():
    for key in board.keys():
        if board[key] == ' ':
            return False
    return True

def insertLetter(letter, position):
    if spaceFree(position):
        board[position] = letter
        printBoard(board)
        if checkDraw():
            print('Draw!')
            return True  # Game over
        elif checkWin():
            if letter == 'X':
                print('Bot wins!')
            else:
                print('You win!')
            return True  # Game over
        return False  # Game continues
    else:
        print('Position taken, please pick a different position.')
        position = int(input('Enter new position: '))
        return insertLetter(letter, position)

player = 'O'
bot = 'X'

def playerMove():
    position = int(input('Enter position for O: '))
    game_over = insertLetter(player, position)
    return game_over

def compMove():
    bestScore = -1000
    bestMove = 0
    for key in board.keys():
        if board[key] == ' ':
            board[key] = bot
            score = minimax(board, False)
            board[key] = ' '
            if score > bestScore:
                bestScore = score
                bestMove = key
    insertLetter(bot, bestMove)

def minimax(board, isMaximizing):
    if checkMoveForWin(bot):
        return 1
    elif checkMoveForWin(player):
        return -1
    elif checkDraw():
        return 0

    if isMaximizing:
        bestScore = -1000
        for key in board.keys():
            if board[key] == ' ':
                board[key] = bot
                score = minimax(board, False)
                board[key] = ' '
                if score > bestScore:
                    bestScore = score
        return bestScore
    else:
        bestScore = 1000
        for key in board.keys():
            if board[key] == ' ':
                board[key] = player
                score = minimax(board, True)
                board[key] = ' '
                if score < bestScore:
                    bestScore = score
        return bestScore

game_over = False
while not game_over:
    compMove()
    if checkWin() or checkDraw():
        break
    game_over = playerMove()
