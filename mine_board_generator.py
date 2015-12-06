import random

def mine_board_generator(width, height):
    mine_field = [[0 for i in range(width)] for i in range(height)]
    for i in range(0, width):
        for j in range(0, height):
            # generate a random number here, and have a chance for the board to be set to "*"
            if (random.randint(0,5) == 0):
                mine_field[i][j] = "*"

    mine_board = [[0 for i in range(width)] for i in range(height)]
    for i in range(0, width):
        for j in range(0, height):
            if mine_field[i][j] != "*":
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        if 0 <= i + k < width and 0 <= j + l < height:
                            if mine_field[i + k][j + l] == "*":
                                mine_board[i][j] += 1

    return mine_field, mine_board
