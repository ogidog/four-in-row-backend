import numpy as np
import copy

from numpy import ndarray

COLS_NUM = 7
ROWS_NUM = 6
EMPTY_CELL = 0
player_id = 1  # 1 - computer, 2 - user


def get_available_row(col, game_fields):
    non_zero_index = np.nonzero(np.array(game_fields[:, col]))[0]
    if len(non_zero_index) == 0:
        return 5
    return non_zero_index[0] - 1


def set_field(player_id: int, col: int, game_fields: ndarray):
    row = get_available_row(col=col, game_fields=game_fields)
    game_fields[row, col] = player_id


def check_win1(moves):
    score = 0
    game_fields = np.zeros((ROWS_NUM, COLS_NUM))
    result = {"terminal_node": False, "score": None, "player_id": None}

    for i in range(len(moves)):
        if i % 2 == 0:
            player_id = 1
            player_moves = int(len(moves) / 2) + 1
        else:
            player_id = 2
            player_moves = int(len(moves) / 2)

        set_field(col=int(moves[i]), player_id=player_id, game_fields=game_fields)

    result["player_id"] = player_id

    for col in range(COLS_NUM):
        for row in range(3):
            if np.count_nonzero(game_fields[row:row + 4, col] == player_id) == 4:
                score += 22
            if np.count_nonzero(game_fields[row:row + 4, col] == player_id) == 3:
                score += 2
            if np.count_nonzero(game_fields[row:row + 4, col] == player_id) == 2:
                score += 1

    for row in range(ROWS_NUM):
        for col in range(4):
            if np.count_nonzero(game_fields[row, col:col + 4] == player_id) == 4:
                score += 22
            if np.count_nonzero(game_fields[row, col:col + 4] == player_id) == 3:
                score += 2
            if np.count_nonzero(game_fields[row, col:col + 4] == player_id) == 2:
                score += 1

    for i in range(3):
        for j in range(4):
            diagonal = np.array(
                [game_fields[5 - i, j], game_fields[4 - i, j + 1], game_fields[3 - i, j + 2],
                 game_fields[2 - i, j + 3]])
            if np.count_nonzero(diagonal == player_id) == 4:
                score += 22
            if np.count_nonzero(diagonal == player_id) == 3:
                score += 2
            if np.count_nonzero(diagonal == player_id) == 2:
                score += 1

    for i in range(3):
        for j in range(4):
            diagonal = np.array(
                [game_fields[i, j], game_fields[i + 1, j + 1], game_fields[i + 2, j + 2], game_fields[i + 3, j + 3]])
            if np.count_nonzero(diagonal == player_id) == 4:
                score += 22
            if np.count_nonzero(diagonal == player_id) == 3:
                score += 2
            if np.count_nonzero(diagonal == player_id) == 2:
                score += 1

        if score >= 22:
            result["terminal_node"] = True

        score = score - player_moves
        if player_id == 1:
            result["score"] = -score
        else:
            result["score"] = score

        return result


def get_optimal_move1(current_moves, ):
    all_moves = copy.deepcopy(current_moves)
    all_scores = [0]
    is_terminal_node = False

    node_terminal_len = -1
    for move in all_moves:
        if len(move) == node_terminal_len:
            break
        for i in range(COLS_NUM):
            all_moves.append(move + str(i))
            check_result = check_win(moves=move + str(i))
            all_scores.append(check_result["score"])
            if check_result["terminal_node"]:
                is_terminal_node = check_result["terminal_node"]

        if is_terminal_node:
            node_terminal_len = len(move + str(i))

    tree_depth = len(all_moves[-1].replace(all_moves[0], ''))

    terminal_scores = copy.deepcopy(all_scores[-7 ** tree_depth:])
    terminal_moves = copy.deepcopy(all_moves[-7 ** tree_depth:])
    is_max = True
    optimal_column = -1
    optimal_move = ''

    for depth in range(tree_depth, 0, -1):
        if depth == 1:
            if (is_max):
                optimal_column = np.argmax(terminal_scores)
                optimal_move = terminal_moves[optimal_column]
            else:
                optimal_column = np.argmin(terminal_scores)
                optimal_move = terminal_moves[optimal_column]
            break

        maxmin_scores = []
        maxmin_moves = []

        for i in range(int(7 ** depth / 7)):
            score_array = terminal_scores[7 * i: 7 * i + 7]
            move_array = terminal_moves[7 * i: 7 * i + 7]

            if (is_max):
                maxmin_scores.append(np.amax(score_array))
                maxmin_moves.append(move_array[np.argmax(score_array)][:-1])
            else:
                maxmin_scores.append(np.amin(score_array))
                maxmin_moves.append(move_array[np.argmin(score_array)][:-1])

        terminal_scores = copy.deepcopy(maxmin_scores)
        terminal_moves = copy.deepcopy(maxmin_moves)
        is_max = not is_max

    return optimal_column, optimal_move


def check_move_availability(moves_values, game_fields):
    null_fields = np.argwhere(moves_values == 0)


def get_score(game_fields):
    score = 0

    # game_fields = np.zeros((ROWS_NUM, COLS_NUM))
    # for i in range(len(moves)):
    #     if i % 2 == 0:
    #         player_id = 1
    #     else:
    #         player_id = 2
    #    set_field(col=int(moves[i]), player_id=player_id, game_fields=game_fields)

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

    return score


def get_bot_move(game_fields):
    scores = []
    max_score = -99999
    bot_move = -1
    for i in range(COLS_NUM):
        game_fields_copy = copy.deepcopy(game_fields)
        set_field(player_id=2, col=int(i), game_fields=game_fields_copy)
        score = get_score(game_fields=game_fields_copy)
        scores.append(score)

    for i in range(COLS_NUM):
        if scores[i] > max_score:
            max_score = scores[i]
            bot_move = i

    return bot_move


moves_seq = ''
game_fields = np.zeros((ROWS_NUM, COLS_NUM))
while True:
    player_move = int(input("Выберите столбец:"))
    if player_move > 6:
        continue

    set_field(player_id=1, col=player_move, game_fields=game_fields)
    optimal_move = get_bot_move(game_fields=game_fields)
    set_field(player_id=2, col=int(optimal_move), game_fields=game_fields)
    print(moves_seq, optimal_move)
    print(game_fields)

# optimal_move = get_bot_move(moves_seq='0')
# optimal_move = get_optimal_move(moves_seq='01122625333')
