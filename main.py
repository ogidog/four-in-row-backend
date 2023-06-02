import numpy as np
from numpy import ndarray
import copy

COLS_NUM = 7
ROWS_NUM = 6


def get_available_row(col, game_fields):
    non_zero_index = np.nonzero(np.array(game_fields[:, col]))[0]
    if len(non_zero_index) == 0:
        return 5

    return non_zero_index[0] - 1


def set_field(player_id: int, col: int, game_fields: ndarray):
    row = get_available_row(col=col, game_fields=game_fields)
    game_fields[row, col] = player_id


def get_score(game_fields):
    score = 0

    for col in range(COLS_NUM):
        for row in range(3):
            if np.count_nonzero(game_fields[row:row + 4, col] == 2) == 4:
                score += 100
            if np.count_nonzero(game_fields[row:row + 4, col] == 2) == 3 and np.count_nonzero(
                    game_fields[row:row + 4, col] == 0) == 1:
                score += 5
            if np.count_nonzero(game_fields[row:row + 4, col] == 2) == 2 and np.count_nonzero(
                    game_fields[row:row + 4, col] == 0) == 2:
                score += 2
            if np.count_nonzero(game_fields[row:row + 4, col] == 1) == 3 and np.count_nonzero(
                    game_fields[row:row + 4, col] == 0) == 1:
                score += -70

    for row in range(ROWS_NUM):
        for col in range(4):
            if np.count_nonzero(game_fields[row, col:col + 4] == 2) == 4:
                score += 100
            if np.count_nonzero(game_fields[row, col:col + 4] == 2) == 3 and np.count_nonzero(
                    game_fields[row, col:col + 4] == 0) == 1:
                score += 5
            if np.count_nonzero(game_fields[row, col:col + 4] == 2) == 2 and np.count_nonzero(
                    game_fields[row, col:col + 4] == 0) == 2:
                score += 2
            if np.count_nonzero(game_fields[row, col:col + 4] == 1) == 3 and np.count_nonzero(
                    game_fields[row, col:col + 4] == 0) == 1:
                score += -70

    for i in range(3):
        for j in range(4):
            diagonal_cols = [j, j + 1, j + 2, j + 3]
            diagonal_rows = [5 - i, 4 - i, 3 - i, 2 - i]
            diagonal = np.array(
                [game_fields[5 - i, j], game_fields[4 - i, j + 1], game_fields[3 - i, j + 2],
                 game_fields[2 - i, j + 3]])

            if np.count_nonzero(diagonal == 2) == 4:
                score += 100
            if np.count_nonzero(diagonal == 2) == 3 and np.count_nonzero(diagonal == 0) == 1:
                score += 5
            if np.count_nonzero(diagonal == 2) == 3 and np.count_nonzero(diagonal == 0) == 2:
                score += 2
            if np.count_nonzero(diagonal == 1) == 3 and np.count_nonzero(diagonal == 0) == 1:
                diagonal_null_col_index = np.argwhere(diagonal == 0)[0][0]
                available_row = get_available_row(col=diagonal_cols[diagonal_null_col_index], game_fields=game_fields)
                if diagonal_rows[diagonal_null_col_index] == available_row:
                    score += -70

    for i in range(3):
        for j in range(4):
            diagonal_cols = [j, j + 1, j + 2, j + 3]
            diagonal_rows = [i, i + 1, i + 2, i + 3]
            diagonal = np.array(
                [game_fields[i, j], game_fields[i + 1, j + 1], game_fields[i + 2, j + 2], game_fields[i + 3, j + 3]])

            if np.count_nonzero(diagonal == 2) == 4:
                score += 100
            if np.count_nonzero(diagonal == 2) == 3 and np.count_nonzero(diagonal == 0) == 1:
                score += 5
            if np.count_nonzero(diagonal == 2) == 2 and np.count_nonzero(diagonal == 0) == 2:
                score += 2
            if np.count_nonzero(diagonal == 1) == 3 and np.count_nonzero(diagonal == 0) == 1:
                diagonal_null_col_index = np.argwhere(diagonal == 0)[0][0]
                available_row = get_available_row(col=diagonal_cols[diagonal_null_col_index], game_fields=game_fields)
                if diagonal_rows[diagonal_null_col_index] == available_row:
                    score += -70

    for row in range(ROWS_NUM):
        for col in range(3):
            if game_fields[row, col] == 0 and game_fields[row, col + 1] == 1 and game_fields[row, col + 2] == 1 and \
                    game_fields[row, col + 3] == 0 and game_fields[row, col + 4] == 0:
                score += -50

    return score


def check_win(game_fields):
    for col in range(COLS_NUM):
        for row in range(3):
            if np.count_nonzero(game_fields[row:row + 4, col] == 2) == 4:
                return 2

            if np.count_nonzero(game_fields[row:row + 4, col] == 1) == 4:
                return 1

    for row in range(ROWS_NUM):
        for col in range(4):
            if np.count_nonzero(game_fields[row, col:col + 4] == 2) == 4:
                return 2

            if np.count_nonzero(game_fields[row, col:col + 4] == 1) == 4:
                return 1

    for i in range(3):
        for j in range(4):
            diagonal = np.array(
                [game_fields[5 - i, j], game_fields[4 - i, j + 1], game_fields[3 - i, j + 2],
                 game_fields[2 - i, j + 3]])
            if np.count_nonzero(diagonal == 2) == 4:
                return 2

            if np.count_nonzero(diagonal == 1) == 4:
                return 1

    for i in range(3):
        for j in range(4):
            diagonal = np.array(
                [game_fields[i, j], game_fields[i + 1, j + 1], game_fields[i + 2, j + 2], game_fields[i + 3, j + 3]])

            if np.count_nonzero(diagonal == 2) == 4:
                return 2

            if np.count_nonzero(diagonal == 1) == 4:
                return 1

    return 0


def get_bot_col(game_fields):
    scores = []
    max_score = -99999
    bot_col = -1
    for i in range(COLS_NUM):
        game_fields_copy = copy.deepcopy(game_fields)
        set_field(player_id=2, col=int(i), game_fields=game_fields_copy)
        score = get_score(game_fields=game_fields_copy)
        scores.append(score)

    for i in range(COLS_NUM):
        if scores[i] > max_score:
            max_score = scores[i]
            bot_col = i

    return bot_col


moves_seq = ''
game_fields = np.zeros((ROWS_NUM, COLS_NUM))

while True:
    player_col = int(input("\nУкажите столбец:"))
    if player_col > 6:
        print("Номер столбца должен быть с 0 по 6.")
        continue

    set_field(player_id=1, col=player_col, game_fields=game_fields)
    winner = check_win(game_fields=game_fields)
    if winner == 1:
        print(game_fields)
        print("\nИгрок №1 победил.")
        break

    bot_col = get_bot_col(game_fields=game_fields)
    set_field(player_id=2, col=int(bot_col), game_fields=game_fields)
    winner = check_win(game_fields=game_fields)
    if winner == 2:
        print(game_fields)
        print("\nИгрок №2 победил.")
        break

    print(game_fields)
