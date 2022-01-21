"""Gomoku code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Jia Hui Yu with functions contributed by Peishuo Cai.  Last modified: Oct. 26, 2020
"""

def is_empty(board):
    for i in board:
        for j in i:
            if j != " ":
                return False

    return True


def is_bounded(board, y_end, x_end, length, d_y, d_x):
    count = 0
    oppo_not_block = True
    if not -1 < y_end + d_y < 8 or not -1 < x_end + d_x < 8:    # check if the end is next to the side of the board
        count += 1  # if yes, add 1 to the block count

    if count == 0 and board[y_end + d_y][x_end + d_x] != " ":   # check if the end is blocked by another character
        count += 1  # if yes, add 1 to the block count

    if not -1 < y_end - length * d_y < 8 or not -1 < x_end - length * d_x < 8:  # check if the starting end is next to the side of the board
        oppo_not_block = False
        count += 1  # if yes, add 1 to the block count, and set oppo_not_block to False

    if oppo_not_block and board[y_end - length * d_y][x_end - length * d_x] != " ": # check if the starting end is blocked by another character
        count += 1  # if yes, add 1 to the block count

    if count == 0:
        return "OPEN"
    elif count == 1:
        return "SEMIOPEN"
    elif count == 2:
        return "CLOSED"




def len_sequence(board,col,y,x,d_y,d_x):

    if d_y == 1 and d_x == 0: #vertical

            while y != 0:
                if board[y - d_y][x] == col:
                    y -= d_y

                else:
                    break

    elif d_y == 0 and d_x == 1: #horizontal

            while x != 0:
                if board[y][x-d_x] == col:
                    x -= d_x

                else:
                    break

    elif d_y == 1 and d_x == 1: #left to right

        while x != 0 and y != 0:
            if board[y - d_y][x - d_x] == col:
                y -= d_y
                x -= d_x

            else:
                break

    elif d_y == 1 and d_x == -1: #right to left

        while x != 7 and y != 0:
            if board[y - d_y][x - d_x] == col:
                y -= d_y
                x -= d_x

            else:
                break



    i = 0
    c = 0

    while 0 <= y + i*d_y <= 7 and 0 <= x + i*d_x <= 7:

        if board[y + i*d_y][x + i*d_x] == col:
            c += 1
            i +=1

        else:
            return c

    return c



def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count = 0
    semi_open_seq_count = 0

    tup = ()
    tup_open = 0
    tup_semi = 0
    y = y_start
    x = x_start

    if y_start + length*d_y > 7:
        return 0,0

    if x_start + length*d_x > 7:
        return 0,0

    i = 0
    c = 0

    while i <= 7:

        if x > 7 or x < 0:

            tup = (tup_open, tup_semi)
            open_seq_count = tup[0]
            semi_open_seq_count = tup[1]
            return open_seq_count, semi_open_seq_count

        if y > 7 or y < 0:

            tup = (tup_open, tup_semi)
            open_seq_count = tup[0]
            semi_open_seq_count = tup[1]
            return open_seq_count, semi_open_seq_count


        if board[y][x] == col:
            c += 1

        else:
            c = 0

        if c == length and c == len_sequence(board,col,y,x,d_y,d_x):

            res = is_bounded(board, y, x, length, d_y, d_x)

            if res == "SEMIOPEN":
                tup_semi += 1

            if res == "OPEN":
                tup_open += 1

            c = 0


        y += d_y
        x += d_x
        i += 1


    tup = (tup_open, tup_semi)
    open_seq_count = tup[0]
    semi_open_seq_count = tup[1]

    return open_seq_count, semi_open_seq_count




def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    i = 0
    j = 0

    while i <= 7:
        d_y = 0
        d_x = 1

        res_row = detect_row(board,col,i,j,length,d_y,d_x)
        res_col = detect_row(board,col,j,i,length,d_x,d_y)

        open_seq_count += res_col[0]
        semi_open_seq_count += res_col[1]
        open_seq_count += res_row[0]
        semi_open_seq_count += res_row [1]

        i += 1

    i = 0
    j = 0

    while i <= 7:
        d_y = 1
        d_x = 1

        res_top = detect_row(board,col,j,i,length,d_y,1)

        res_top2 = detect_row(board,col,j,i,length,d_y,-1)


        open_seq_count += res_top[0]
        semi_open_seq_count += res_top[1]
        open_seq_count += res_top2[0]
        semi_open_seq_count += res_top2[1]

        i += 1


    h = 1

    while h <= 7:
        d_y = 1
        d_x = 1

        res_left = detect_row(board,col,h,0,length,d_y,1)

        res_right = detect_row(board,col,h,7,length,d_y,-1)


        open_seq_count += res_left[0]
        semi_open_seq_count += res_left[1]
        open_seq_count += res_right[0]
        semi_open_seq_count += res_right[1]

        h += 1

    return open_seq_count, semi_open_seq_count


def freesquares(board):

    freesquares = []

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == " ":
                freesquares.append([i, j])

    return freesquares

def copy(board):
    copy = [[],[],[],[],[],[],[],[]]

    for i in range(len(board)):
        for j in range(len(board[0])):
            copy[i].append(board[i][j])

    return copy


def search_max(board):
    options = freesquares(board)
    potentialscores = []


    for i in options:
        trialboard = copy(board)
        trialboard[i[0]][i[1]] = "b"

        potentialscores.append(score(trialboard))


    best = potentialscores.index(max(potentialscores))
    move_y = options[best][0]
    move_x = options[best][1]
    return move_y, move_x


def score(board): #
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE


    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def five(board, col):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if len_sequence(board,col,i,j,1,0) == 5:
                return True
            elif len_sequence(board,col,i,j,0,1) == 5:
                return True
            elif len_sequence(board,col,i,j,1,1) == 5:
                return True
            elif len_sequence(board,col,i,j,1,-1) == 5:
                return True

    return False


def is_win(board):
    if freesquares(board) == []:
        return "Draw"

    elif detect_rows(board,"b",5) != (0,0):
        return "Black won"

    elif detect_rows(board,"w",5) != (0,0):
        return "White won"

    elif five(board,"b"):
        return "Black won"

    elif five(board,"w"):
        return "White won"

    else:
        return "Continue playing"

def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))




def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res


        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0

def testboard():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)

    return board

def testing_win_5_closed():
    board = make_empty_board(8)
    board[2][2] = "w"
    y = 3;
    x = 2;
    d_x = 0;
    d_y = 1;
    length = 5
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    if is_win(board)=="Black won":
        print("PASSSSSSSSS")
    else:
        print("EPIC FAIL :(")
        # Expected output:
        # *0|1|2|3|4|5|6|7*
        # 0 | | | | | | | *
        # 1 | | | | | | | *
        # 2 | |w| | | | | *
        # 3 | |b| | | | | *
        # 4 | |b| | | | | *
        # 5 | |b| | | | | *
        # 6 | |b| | | | | *
        # 7 | |b| | | | | *
        # *****************
        # PASSSSSSSSS



if __name__ == '__main__':

    y = [[' ', ' ', ' ', ' ', ' ', ' ', 'w', ' '], [' ', ' ', ' ', ' ', ' ', 'w', ' ', ' '], [' ', ' ', ' ', ' ', 'w', ' ', ' ', ' '], [' ', ' ', ' ', 'w', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    print(is_bounded(y,3,3,4,1,-1))

    b = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['b', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', 'b', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', 'b', ' ', ' ', ' ', ' ', ' ']]
    print(is_bounded(b,7,2,3,1,1))


    k = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', 'b', 'b', 'b', ' ', ' ', ' ', ' '], [' ', ' ', ' ', 'b', ' ', ' ', ' ', ' '], [' ', ' ', ' ', 'b', ' ', ' ', ' ', ' '], [' ', ' ', ' ', 'w', ' ', 'b', ' ', ' '], [' ', ' ', 'b', ' ', 'b', ' ', ' ', ' '], [' ', ' ', ' ', 'b', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', 'b', ' ', ' ', ' ']]
    print_board(k)
    print(detect_rows(k,"b",3))
    print("should be 2,2")
    print(detect_rows(k,"b",2))
    print("should be 1,0")

    l = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['b', ' ', ' ', ' ', ' ', 'w', ' ', ' '], [' ', 'b', ' ', ' ', ' ', 'w', ' ', ' '], [' ', ' ', 'b', ' ', ' ', 'w', ' ', ' ']]
    print_board(l)
    print(detect_row(l,"w",0,5,3,1,0))
    print("should be 0,1")

    x = testboard()
    x[1][7] = "b"
    print_board(x)
    # print(score(x))
    detect_rows(x,"b",2)
    # search_max(x)
    testing_win_5_closed()
analysis(
[[' ', 'b', 'w', 'w', 'w', 'w', 'w', 'b'], ['b', 'b', ' ', 'w', 'w', 'w', 'w', 'b'], ['b', 'b', 'w', 'w', ' ', ' ', ' ', 'b'], ['b', 'b', ' ', 'w', ' ', ' ', ' ', 'b'], ['b', 'b', ' ', 'b', ' ', 'b', ' ', 'w'], ['b', ' ', 'b', 'b', 'b', 'b', 'b', 'w'], ['w', ' ', ' ', 'b', 'w', 'b', 'b', ' '], [' ', 'w', 'b', ' ', 'w', 'w', ' ', ' ']])











