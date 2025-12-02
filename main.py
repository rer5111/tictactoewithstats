import os, random, time, copy

dir = os.listdir()
if "tictactoe_stats" not in dir:
    os.mkdir(".\\tictactoe_stats")
try:
    with open("tictactoe_stats\stats.txt", "r") as stats:
        statlist = stats.readlines()
        games_won = int(statlist[1])
        games_played = int(statlist[3])
        xs_played = int(statlist[5])
        os_played = int(statlist[7])
except:
    try:
        file = open("tictactoe_stats\stats.txt", "x")
        file.close
    except:
        pass
    games_won = 0
    games_played = 0
    xs_played = 0
    os_played = 0

def display_board():
    print(" ", end=" ")
    for i in range(boardsize):
        print(i+1, end=" ")
    for i, n in enumerate(board):
        print(f"\n{i+1}", end=" ")
        for j in n:
            if j == 0:
                print("-", end=" ")
            else:
                print(j, end=" ")

class Oponent():
    def __init__(self, is_x):
        self.prev_turn = []
        self.is_x = is_x

    def make_turn(self, board : list) -> str:
        if self.prev_turn == []:
            print("we doin starter")
            if random.randint(1, 9) > 4:
                return (random.randint(1, len(board)-1), random.randint(1, len(board)-1))
            else:
                if random.choice([True, False]):
                    return (random.randint(0, len(board)-1), 0)
                else:
                    return (0, random.randint(0, len(board)-1))
        else:
            for i, n in enumerate(board):
                for j, n2 in enumerate(board):
                    if board[i][j] == 0:
                        checkboard = copy.deepcopy(board)
                        if self.is_x:
                            checkboard[i][j] = "o"
                            if check_win(checkboard):
                                return (i, j)
                            checkboard[i][j] = "x"
                            if check_win(checkboard):
                                return (i, j)
                        else:
                            checkboard[i][j] = "x"
                            if check_win(checkboard):
                                return (i, j)
                            checkboard[i][j] = "o"
                            if check_win(checkboard):
                                return (i, j)
            x, y = self.prev_turn
            tempturn = []
            for i in range(-1, 1):
                for j in range(-1, 1):
                    if i+j != 0 and boardget((i, j), board) != -1:
                        tempturn.append((i, j))
            if len(tempturn) == 0:
                while True:
                    x, y = random.randint(0, len(board)-1), random.randint(0, len(board)-1)
                    if boardget((x, y), board) == 0:
                        break
                return (x, y)
            else:
                return random.choice(tempturn)



    

def check_win(board: list) -> str:
    for i, n in enumerate(board):
        for j, n2 in enumerate(n):
            if n2 != 0:
                if check_win_til(board, (i, j), (0, 0), 3):
                    print("win found")
                    return 1

def boardget(tile : tuple[int, int], board: list[list]) -> str:
    x, y = tile
    if (0 <= x < len(board)) and (0 <= y < len(board)):
        return board[x][y]
    else:
        return -1 
                
def check_win_til(board, tile, step, towin):
    rw, cl = tile
    x, y = step
    if towin == 3:
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i != 0 or j != 0:
                    if check_win_til(board, (rw+i, cl+j), (i, j), 2):
                        return 1
    elif towin > 0:
        if boardget((rw-x, cl-y), board) == boardget((rw, cl), board):
            if check_win_til(board, (rw-x, cl-y), (x, y), towin-1):
                return 1
            else:
                return 0
        else:
            return 0
    else:
        return 1
    return 0

running = True
while running:
        try:
            inp = int(input("Какой режим вы хотите выбрать?\n1. Против робота.\n2. Против игрока.\n0. Выйти\n>>> "))
        except:
            print("Неверное число!")
        if inp == 1:
            p1turn = random.choice([True, False])
            while True:
                x_p1 = p1turn
                if x_p1:
                    print("Вы - Крестики")
                else:
                    print("Вы - Нолики")
                try:
                    inp = int(input("Введите размер игрового поля (3-9):\n>>> "))
                except:
                    print("Неверное число!")
                if inp < 3 or inp > 9:
                    print("Введите число от 3 до 9!")
                else:
                    boardsize = inp
                    board = []
                    for i in range(boardsize):
                        board.append([])
                        for j in range(boardsize):
                            board[i].append(0)
                    oponent = Oponent(not x_p1)
                    break
            while True:
                if p1turn:
                    print("Ход игрока!")
                    while True:
                        display_board()
                        inp = input("\nВведите ряд и столбец, в котором вы хотите походить. Формат: (35 -> Ряд 3 Столбец 5)\n>>> ")
                        try:
                            rw = int(inp[0])-1
                            cl = int(inp[1])-1
                            if (0 <= rw <= boardsize) and (0 <= cl <= cl):
                                if board[rw][cl] == 0:
                                    if x_p1:
                                        board[rw][cl] = "x"
                                    else:
                                        board[rw][cl] = "o"
                                    break
                            else:
                                print("Это место уже занято!")
                        except:
                            print("Введите ряд и столбец в правильном формате!")
                else:
                    print("Ход робота!")
                    while True:
                        x_r, y_r = oponent.make_turn(board)
                        if boardget((x_r, y_r), board) == 0:
                            break
                    oponent.prev_turn = [x_r, y_r]
                    if not x_p1:
                        board[x_r][y_r] = "x"
                    else:
                        board[x_r][y_r] = "o"
                if (p1turn and x_p1) or (not p1turn and not x_p1):
                    xs_played+=1
                else:
                    os_played+=1
                if check_win(board):
                    if p1turn:
                        display_board()
                        print()
                        if x_p1:
                            print("Победили крестики!")
                        else:
                            print("Победили нолики!")
                    else:
                        display_board()
                        print()
                        if x_p1:
                            print("Победили нолики!")
                        else:
                            print("Победили крестики!")
                    games_played += 1
                    if p1turn:
                        games_won += 1
                    break
                p1turn = not p1turn
                    

        elif inp == 2:
            turn = True
            while True:
                try:
                    inp = int(input("Введите размер игрового поля (3-9):\n>>> "))
                except:
                    print("Неверное число!")
                if inp < 3 or inp > 9:
                    print("Введите число от 3 до 9!")
                else:
                    boardsize = inp
                    board = []
                    for i in range(boardsize):
                        board.append([])
                        for j in range(boardsize):
                            board[i].append(0)
                    break
            while True:
                if turn:
                    print("Ход крестиков!")
                else:
                    print("Ход ноликов!")
                while True:
                    display_board()
                    inp = input("\nВведите ряд и столбец, в котором вы хотите походить. Формат: (35 -> Ряд 3 Столбец 5)\n>>> ")
                    try:
                        rw = int(inp[0])-1
                        cl = int(inp[1])-1
                        if (0 <= rw <= boardsize) and (0 <= cl <= cl):
                            if board[rw][cl] == 0:
                                if turn:
                                    board[rw][cl] = "x"
                                else:
                                    board[rw][cl] = "o"
                                break
                        else:
                            print("Это место уже занято!")
                    except:
                        print("Введите ряд и столбец в правильном формате!")
                if turn:
                    xs_played+=1
                else:
                    os_played+=1
                if check_win(board):
                    if turn:
                        print("Победили крестики!")
                    else:
                        print("Победили нолики!")
                    games_played+= 1
                    break
                turn = not turn
        elif inp == 0:
            running = False
        else:
            print("Введите число от 0 до 2!")

results = f"сыграно игр (всего):\n{games_played}\nвыиграно игр (против робота):\n{games_won}\nпоставлено крестиков:\n{xs_played}\nпоставлено ноликов:\n{os_played}"
with open("tictactoe_stats\stats.txt", "w") as stats:
    stats.write(results)