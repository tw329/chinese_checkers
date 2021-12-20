import matplotlib.pyplot as plt
from numpy import *
import math
from itertools import permutations, repeat
import re
import os
import imageio

# Define empty space
def empty(i, j):
    if ([i, j] not in movable_piece) and ([i, j] not in piece) and ([i, j] not in out_of_board):
        return 1
    else:
        return 0

# Define the space outside the board
out_of_board = []
for i in range(-10, 11):
    for j in range(-10, 11):
        if i <= -5 and j <= 0 :
            out_of_board.append([i, j])
        elif i in range(-4, 1) and j <= -5:
            out_of_board.append([i, j])
        elif i in range(0, 11) and j >= 5:
            out_of_board.append([i, j])
        elif i >= 5 and j in range(0, 5):
            out_of_board.append([i, j])
        elif i in range(5, 11) and j in range(-10, -4):
            out_of_board.append([i, j])
        elif i in range(-10, -4) and j in range(5, 11):
            out_of_board.append([i, j])
        elif (i == -10 or i == -9) and j in range(-1, 5):
            out_of_board.append([i, j])
        elif i == -8 and j in range(1, 4):
            out_of_board.append([i, j])
        elif i == -7 and j in range(1, 3):
            out_of_board.append([i, j])
        elif i == -6 and j == 1:
            out_of_board.append([i, j])
        elif i == -4 and j in range(9, 11):
            out_of_board.append([i, j])
        elif i == -3 and j in range(8, 11):
            out_of_board.append([i, j])
        elif i == -2 and j in range(7, 11):
            out_of_board.append([i, j])
        elif i == -1 and j in range(6, 11):
            out_of_board.append([i, j])
        elif i == 1 and j in range(-10, -5):
            out_of_board.append([i, j])
        elif i == 2 and j in range(-10, -6):
            out_of_board.append([i, j])
        elif i == 3 and j in range(-10, -7):
            out_of_board.append([i, j])
        elif i == 4 and j in range(-10, -8):
            out_of_board.append([i, j])
        elif i == 6 and j == -1:
            out_of_board.append([i, j])
        elif i == 7 and j in range(-2, 0):
            out_of_board.append([i, j])
        elif i == 8 and j in range(-3, 0):
            out_of_board.append([i, j])
        elif (i == 9 or i == 10) and j in range(-4, 0):
            out_of_board.append([i, j])
# List all the possible moves
def move_basic(x, y):
    where = []
    if empty(x-1, y+1) == 1:
        where.append([x-1, y+1, "move"])
    if empty(x-1, y) == 1:
        where.append([x-1, y, "move"])
    if empty(x+1, y-1) == 1:
        where.append([x+1, y-1, "move"])
    if empty(x, y+1) == 1:
        where.append([x, y+1, "move"])
    if empty(x, y-1) == 1:
        where.append([x, y-1, "move"])
    if empty(x+1, y) == 1:
        where.append([x+1, y, "move"])
    if (empty(x-1, y+1) == 0) and (empty(x-2, y+2) == 1):
        where.append([x-2, y+2, "jump"])
    if (empty(x-1, y) == 0) and (empty(x-2, y) == 1):
        where.append([x-2, y, "jump"])
    if (empty(x+1, y-1) == 0) and (empty(x+2, y-2) == 1):
        where.append([x+2, y-2, "jump"])
    if (empty(x, y+1) == 0) and (empty(x, y+2) == 1):
        where.append([x, y+2, "jump"])
    if (empty(x, y-1) == 0) and (empty(x, y-2) == 1):
        where.append([x, y-2, "jump"])
    if (empty(x+1, y) == 0) and (empty(x+2, y) == 1):
        where.append([x+2, y, "jump"])

    return where

# See where can the pieces move
def move_where(x, y):
    where = []
    for i in range(len(move_basic(x, y))):
        where.append(move_basic(x, y)[i])
        if where[i][2] == "jump":
            for j in range(len(move_basic(where[i][0], where[i][1]))):
                where.append(move_basic(where[i][0], where[i][1])[j])
            for k in reversed(range(len(where))):
                if where[k][2] == "move" and k > i:
                    del where[k]
    return where

# Calculate the score
def score(new = []):
    score = 0
    empty_target = []
    piece_not_target = []
    for i in range(len(target_1)):
        if target_1[i] not in new:
            empty_target.append(target_1[i])
    for j in range(len(new)):
        if new[j] not in target_1:
            piece_not_target.append(new[j])
        score += abs(linalg.norm(array(new[j]) - array(target_1[0])))
    for k in range(len(piece_not_target)):
        score += (abs(linalg.norm(array(empty_target[k]) - array(piece_not_target[k]))) * 100)
    for l in range(len(new)):
        if new[l] in start_piece:
            score += 70
    return score

# If all the pieces are in the target then game over
def win(x = []):
    for i in range(len(x)):
        if x[i] not in target_1:
            return False
    return True

# Move the pieces
# Return the score after move, pieces location before move, pieces location after move
def move():
    temp = [score(movable_piece), 0, 0]
    for i in range(len(movable_piece)):
        for j in range(len(move_where(movable_piece[i][0], movable_piece[i][1]))):
            temp_piece = [[move_where(movable_piece[i][0], movable_piece[i][1])[j][0],
                           move_where(movable_piece[i][0], movable_piece[i][1])[j][1]]
                          if x == [movable_piece[i][0], movable_piece[i][1]] else x
                          for x in movable_piece]
            if (score(temp_piece) < temp[0]):
                temp[0] = score(temp_piece)
                temp[1] = i
                temp[2] = j
    return temp

# Plot
def draw(drawfilename):
    test = 1
    t = str(test)
    for j in range(-10, 11):
        for i in range(-10, 11):
            if [i, j] in movable_piece:
                plt.scatter(i, j, marker='o', c = 'm')
            elif [i, j] in target_1:
                plt.scatter(i, j, marker='^', facecolors = 'none', edgecolors = 'g')
            elif [i, j] in piece:
                plt.scatter(i, j, marker='o', c = 'r')
            elif empty(i, j) == 1:
                plt.scatter(i, j, marker='o', facecolors = 'none', edgecolors = 'b')
            elif empty(i, j) == 0:
                plt.scatter(i, j, marker='x', c = 'k')
    plt.savefig(drawfilename)
    plt.clf()

num = ['S1', 'S2', 'S3', 'S4']
for topic in num:
    if topic == 'S1':
        movable_piece  = [[4, -8], [4, -7], [3, -7], [4, -6], [3, -6], [2, -6], [4, -5], [3, -5], [2, -5], [1, -5], [4, -4], [3, -4], [2, -4], [1, -4], [0, -4]]
        start_piece =  [[0, -4], [1, -4], [2, -4], [3, -4], [4, -4], [1, -5], [2, -5], [3, -5], [4, -5], [2, -6], [3, -6], [4, -6], [3, -7], [4, -7], [4, -8]]
        target_1 = [[-4, 8], [-4, 7], [-3, 7], [-4, 6], [-3, 6], [-2, 6], [-4, 5], [-3, 5], [-2, 5], [-1, 5], [-4, 4], [-3, 4], [-2, 4], [-1, 4], [0, 4]]
        piece = []
        # Target
        sum_target_x = 0
        sum_target_y = 0
        for i in range(len(target_1)):
            sum_target_x += target_1[i][0]
            sum_target_y += target_1[i][1]
        t_avrg_x = sum_target_x/len(movable_piece)
        t_avrg_y = sum_target_y/len(movable_piece)
        t_avrg = array([t_avrg_x, t_avrg_y])
        count = 0
        f = open('result_1.txt', 'w')
        drawfiles = []
        while win(movable_piece) == False:
            count += 1
            temp = move()
            a = str([movable_piece[temp[1]][0], movable_piece[temp[1]][1]])
            b = str([move_where(movable_piece[temp[1]][0], movable_piece[temp[1]][1])[temp[2]][0],
                    move_where(movable_piece[temp[1]][0], movable_piece[temp[1]][1])[temp[2]][1]])
            f = open('result_1.txt', 'a')
            f.write(a + ";" + b + "\n")
            movable_piece = [[move_where(movable_piece[temp[1]][0], movable_piece[temp[1]][1])[temp[2]][0],
                              move_where(movable_piece[temp[1]][0], movable_piece[temp[1]][1])[temp[2]][1]]
                             if x == [movable_piece[temp[1]][0], movable_piece[temp[1]][1]]
                             else x
                             for x in movable_piece]
            drawfilename = f'{topic}_{count}.png'
            draw(drawfilename)
            drawfiles.append(drawfilename)
            
        with imageio.get_writer('S1.gif', mode='I') as writer:
            for filename in drawfiles:
                image = imageio.imread(filename)
                writer.append_data(image)
        for filename in set(drawfiles):
            os.remove(filename)

    elif topic == 'S2':
        movable_piece  = [[4, -8], [4, -7], [3, -7], [4, -6], [3, -6], [2, -6], [4, -5], [3, -5], [2, -5], [1, -5], [4, -4], [3, -4], [2, -4], [1, -4], [0, -4]]
        start_piece =  [[0, -4], [1, -4], [2, -4], [3, -4], [4, -4], [1, -5], [2, -5], [3, -5], [4, -5], [2, -6], [3, -6], [4, -6], [3, -7], [4, -7], [4, -8]]
        target_1 = [[-8, 4], [-7, 4], [-7, 3], [-6, 4], [-6, 3], [-6, 2], [-5, 4], [-5, 3], [-5, 2], [-5, 1], [-4, 4], [-4, 3], [-4, 2], [-4, 1], [-4, 0]]
        piece = []
        # Target
        sum_target_x = 0
        sum_target_y = 0
        for i in range(len(target_1)):
            sum_target_x += target_1[i][0]
            sum_target_y += target_1[i][1]
        t_avrg_x = sum_target_x/len(movable_piece)
        t_avrg_y = sum_target_y/len(movable_piece)
        t_avrg = array([t_avrg_x, t_avrg_y])
        count = 0
        f = open('result_2.txt', 'w')
        drawfiles = []
        while win(movable_piece) == False:
            count += 1
            temp = move()
            a = str([movable_piece[temp[1]][0], movable_piece[temp[1]][1]])
            b = str([move_where(movable_piece[temp[1]][0], movable_piece[temp[1]][1])[temp[2]][0],
                    move_where(movable_piece[temp[1]][0], movable_piece[temp[1]][1])[temp[2]][1]])
            f = open('result_2.txt', 'a')
            f.write(a + ";" + b + "\n")
            movable_piece = [[move_where(movable_piece[temp[1]][0], movable_piece[temp[1]][1])[temp[2]][0],
                              move_where(movable_piece[temp[1]][0], movable_piece[temp[1]][1])[temp[2]][1]]
                             if x == [movable_piece[temp[1]][0], movable_piece[temp[1]][1]]
                             else x
                             for x in movable_piece]
            drawfilename = f'{topic}_{count}.png'
            draw(drawfilename)
            drawfiles.append(drawfilename)

        with imageio.get_writer('S2.gif', mode='I') as writer:
            for filename in drawfiles:
                image = imageio.imread(filename)
                writer.append_data(image)
        for filename in set(drawfiles):
            os.remove(filename)
    elif topic == 'S3':
        movable_piece  = [[4, -8], [4, -7], [3, -7], [4, -6], [3, -6], [2, -6], [4, -5], [3, -5], [2, -5], [1, -5], [4, -4], [3, -4], [2, -4], [1, -4], [0, -4]]
        start_piece =  [[0, -4], [1, -4], [2, -4], [3, -4], [4, -4], [1, -5], [2, -5], [3, -5], [4, -5], [2, -6], [3, -6], [4, -6], [3, -7], [4, -7], [4, -8]]
        target_1 = [[-4, 8], [-4, 7], [-3, 7], [-4, 6], [-3, 6], [-2, 6], [-4, 5], [-3, 5], [-2, 5], [-1, 5], [-4, 4], [-3, 4], [-2, 4], [-1, 4], [0, 4]]

        read_3 = open('obstacle.txt', 'r')
        x = read_3.readlines()
        temp = []
        piece = []
        pat = '\-*\d+'
        for i in range(len(x)):
            if i != 0:
                for j in re.findall(pat, x[i]):
                    temp.append(int(j))
                piece.append(temp)
                temp = []
        # Target
        sum_target_x = 0
        sum_target_y = 0
        for i in range(len(target_1)):
            sum_target_x += target_1[i][0]
            sum_target_y += target_1[i][1]
        t_avrg_x = sum_target_x/len(movable_piece)
        t_avrg_y = sum_target_y/len(movable_piece)
        t_avrg = array([t_avrg_x, t_avrg_y])
        count = 0
        f = open('result_3.txt', 'w')
        drawfiles = []
        while win(movable_piece) == False:
            count += 1
            temp = move()
            a = str([movable_piece[temp[1]][0], movable_piece[temp[1]][1]])
            b = str([move_where(movable_piece[temp[1]][0], movable_piece[temp[1]][1])[temp[2]][0],
                    move_where(movable_piece[temp[1]][0], movable_piece[temp[1]][1])[temp[2]][1]])
            f = open('result_3.txt', 'a')
            f.write(a + ";" + b + "\n")
            movable_piece = [[move_where(movable_piece[temp[1]][0], movable_piece[temp[1]][1])[temp[2]][0],
                              move_where(movable_piece[temp[1]][0], movable_piece[temp[1]][1])[temp[2]][1]]
                             if x == [movable_piece[temp[1]][0], movable_piece[temp[1]][1]]
                             else x
                             for x in movable_piece]
            drawfilename = f'{topic}_{count}.png'
            draw(drawfilename)
            drawfiles.append(drawfilename)

        with imageio.get_writer('S3.gif', mode='I') as writer:
            for filename in drawfiles:
                image = imageio.imread(filename)
                writer.append_data(image)
        for filename in set(drawfiles):
            os.remove(filename)

    elif topic == 'S4':
        read_4 = open('initial.txt', 'r')
        x = read_4.readlines()
        temp = []
        movable_piece = []
        pat = '\-*\d+'
        for i in range(len(x)):
            if i != 0:
                for j in re.findall(pat, x[i]):
                    temp.append(int(j))
                movable_piece.append(temp)
                temp = []
        target_1 = [[-4, -4], [-4, -3], [-3, -4], [-4, -2], [-3, -3], [-2, -4], [-4, -1], [-3, -2], [-2, -3], [-1, -4], [-4, 0], [-3, -1], [-2, -2], [-1, -3], [0, -4]]
        start_piece = []
        for i in movable_piece:
            start_piece.append(i)
        piece = []
        # Target
        sum_target_x = 0
        sum_target_y = 0
        for i in range(len(target_1)):
            sum_target_x += target_1[i][0]
            sum_target_y += target_1[i][1]
        t_avrg_x = sum_target_x/len(movable_piece)
        t_avrg_y = sum_target_y/len(movable_piece)
        t_avrg = array([t_avrg_x, t_avrg_y])
        count = 0
        f = open('result_4.txt', 'w')
        drawfiles = []
        while win(movable_piece) == False:
            count += 1
            temp = move()
            a = str([movable_piece[temp[1]][0], movable_piece[temp[1]][1]])
            b = str([move_where(movable_piece[temp[1]][0], movable_piece[temp[1]][1])[temp[2]][0],
                    move_where(movable_piece[temp[1]][0], movable_piece[temp[1]][1])[temp[2]][1]])
            f = open('result_4.txt', 'a')
            f.write(a + ";" + b + "\n")
            movable_piece = [[move_where(movable_piece[temp[1]][0], movable_piece[temp[1]][1])[temp[2]][0],
                              move_where(movable_piece[temp[1]][0], movable_piece[temp[1]][1])[temp[2]][1]]
                             if x == [movable_piece[temp[1]][0], movable_piece[temp[1]][1]]
                             else x
                             for x in movable_piece]
            drawfilename = f'{topic}_{count}.png'
            draw(drawfilename)
            drawfiles.append(drawfilename)

        with imageio.get_writer('S4.gif', mode='I') as writer:
            for filename in drawfiles:
                image = imageio.imread(filename)
                writer.append_data(image)
        for filename in set(drawfiles):
            os.remove(filename)