import random
import pygame


EDGE = 400  # size of window
WIN = pygame.display.set_mode((EDGE, EDGE))  # Window
pygame.display.set_caption("tic-tac-toe!")  # Title

# Colour settings
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (128, 128, 128)


class Node:
    def __init__(self, row, col, edge, color):  # initialize the variables
        self.row = row
        self.col = col
        self.x = row * edge
        self.y = col * edge
        self.color = color
        self.edge = edge

    def get_pos(self):  # initialize the variables
        return self.row, self.col

    def draw(self, win):  # draw the window and the grid with size 1
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.edge, self.edge))

    def is_empty(self):
        return self.color == WHITE

    def is_Player0(self):  # condition by colour
        return self.color == BLACK

    def is_Player1(self):  # condition by colour
        return self.color == RED

    def make_Player0(self):  # set colour for the action
        self.color = BLACK

    def make_Player1(self):  # set colour for the action
        self.color = RED


def make_grid(rows, edge):  # set how many rows and divided the whole screen to grid
    grid = []
    gap = edge // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, WHITE)
            grid[i].append(node)
    return grid


def draw_grid(win, rows, edge):  # draw grid from 0 to size of edge in each gap on row and colum
    gap = edge // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (edge, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, edge))


def draw(win, grid, rows, edge):  # fill the grid with White
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, edge)
    pygame.display.update()


def get_clicked_pos(pos, rows, edge):  # set each cube in the grid as a position
    gap = edge // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def get_board_from_grid(grid):  # get the board from the grid
    board = []  # list
    for row in grid:
        board_row = []
        for node in row:  # for each node use symbol as determination
            if node.is_empty():
                board_row.append('.')
            elif node.is_Player0():
                board_row.append('O')
            else:
                board_row.append('X')
        board.append(board_row)
    return board


def get_copy_board(board):  # copy the board for the literation
    new_board = []
    for row in board:
        new_row = []
        for col in row:
            new_row.append(col)
        new_board.append(new_row)
    return new_board


def get_next_player(player):  # moves 1 by 1
    if player == 'X':
        return 'O'
    return "X"


def get_valid_move_board(board, player):  # check the valid place to place the move
    res = []
    board_res = []
    for row_index in range(len(board)):
        for col_index in range(len(board)):
            if board[row_index][col_index] == '.':
                res.append((row_index, col_index))
                new_board = get_copy_board(board)
                new_board[row_index][col_index] = player
                board_res.append(new_board)
    return res, board_res


def get_board_str(board):
    str = ""
    for row in board:
        str += ''.join(row)
    return str


def make_mc_move(grid):  # make a move using mc method
    board = get_board_from_grid(grid) # get board according to grid
    res_score = {}
    for iteration in range(10000):
        # iteration
        player = 'X'
        first_move = None # get first move
        next_moves, next_board = get_valid_move_board(board, player) # get available moves for curr state
        curr_score = 9 # set init score
        while len(next_board) != 0:
            index = random.randint(0, len(next_board)-1) # random action
            if first_move is None:
                first_move = next_moves[index] # get first move
            curr_score = curr_score - 1 # the earlier you win, the more score you get
            end = is_board_end(next_board[index])
            if end != 0:
                if end == 3:
                    curr_score = 0
                if end == 1:
                    curr_score = -curr_score
                break
            player = get_next_player(player)
            next_moves, next_board = get_valid_move_board(next_board[index], player)
        if first_move not in res_score:
            # store the move and score
            res_score[first_move] = [0, 0]
        res_score[first_move][0] += 1
        res_score[first_move][1] += curr_score

    # find best move
    best_move = None
    best_score = -100000000000
    for key, value in res_score.items():
        # find move that has best average score
        if value[1] / value[0] > best_score:
            best_move = key
            best_score = value[1] / value[0]
    grid[best_move[0]][best_move[1]].make_Player1()


def is_board_end(board):  # check if the board is end
    # 0. not end
    # 1. user wins
    # 2. computer wins
    # 3. tie
    # 1. check user win
    user_win = list('OOO')
    computer_win = list('XXX')
    for row in board:
        if row == user_win:
            return 1
    for i in range(len(board)):
        col = [row[i] for row in board]
        if col == user_win:
            return 1
    diag = [board[0][0], board[1][1], board[2][2]]
    if diag == user_win:
        return 1
    diag = [board[2][0], board[1][1], board[0][2]]
    if diag == user_win:
        return 1

    # 2. check computer win
    for row in board:
        if row == computer_win:
            return 2
    for i in range(len(board)):
        col = [row[i] for row in board]
        if col == computer_win:
            return 2
    diag = [board[0][0], board[1][1], board[2][2]]
    if diag == computer_win:
        return 2
    diag = [board[2][0], board[1][1], board[0][2]]
    if diag == computer_win:
        return 2

    # 3. check tie or not
    has_empty = False
    for row in board:
        for col in row:
            if col == '.':
                has_empty = True
    if has_empty:
        return 0
    else:
        return 3


def is_end(grid):  # is end or not
    board = get_board_from_grid(grid)
    return is_board_end(board)


def main(win, edge):  # main
    nog = 3  # number of grids
    grid = make_grid(nog, edge)  # make grid

    running = True
    end = 0

    while running:  # keep looping the main program
        draw(win, grid, nog, edge)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # if quit end the loop
                running = False

            if pygame.mouse.get_pressed()[0]:  # if press left mouse button
                pos = pygame.mouse.get_pos()  # get position based on grid
                row, col = get_clicked_pos(pos, nog, edge)
                node = grid[row][col]
                if node.is_empty():  # user make move
                    node.make_Player0()
                    end = is_end(grid)
                    if end == 0:
                        make_mc_move(grid)  # make move use monte carlo
                    end = is_end(grid)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:  # if press c
                    end = 0
                    grid = make_grid(nog, edge)

        if end != 0:
            if end == 1:
                message = "User wins!"
            elif end == 2:
                message = "Computer wins!"
            else:
                message = "Tie!"
            print(message)
            end = 0


main(WIN, EDGE)  # call main
