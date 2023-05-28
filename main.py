import numpy as np
import copy

from numpy import ndarray

COLS_NUM = 7
ROWS_NUM = 6
EMPTY_CELL = 0
player_id = 1  # 1 - computer, 2 - user


def get_available_row(col, game_field):
    non_zero_index = np.nonzero(np.array(game_field[:, col]))[0]
    if len(non_zero_index) == 0:
        return 5
    return non_zero_index[0] - 1


def set_field(player_id: int, col: int, game_field: ndarray):
    row = get_available_row(col=col, game_field=game_field)
    game_field[row, col] = player_id


def check_win(moves):
    score = 0
    game_field = np.zeros((ROWS_NUM, COLS_NUM))
    result = {"terminal_node": False, "score": None, "player_id": None}

    for i in range(len(moves)):
        if i % 2 == 0:
            player_id = 1
            player_moves = int(len(moves) / 2) + 1
        else:
            player_id = 2
            player_moves = int(len(moves) / 2)

        set_field(col=int(moves[i]), player_id=player_id, game_field=game_field)

    result["player_id"] = player_id

    for col in range(COLS_NUM):
        for row in range(3):
            if np.count_nonzero(game_field[row:row + 4, col] == player_id) == 4:
                score += 100
            if np.count_nonzero(game_field[row:row + 4, col] == player_id) == 3:
                score += 7
            if np.count_nonzero(game_field[row:row + 4, col] == player_id) == 2:
                score += 2

    for row in range(ROWS_NUM):
        for col in range(4):
            if np.count_nonzero(game_field[row, col:col + 4] == player_id) == 4:
                score += 100
            if np.count_nonzero(game_field[row, col:col + 4] == player_id) == 3:
                score += 7
            if np.count_nonzero(game_field[row, col:col + 4] == player_id) == 2:
                score += 2

    for i in range(3):
        for j in range(4):
            positive_diagonal = np.array(
                [game_field[5 - i, j], game_field[4 - i, j + 1], game_field[3 - i, j + 2], game_field[2 - i, j + 3]])
            if np.count_nonzero(positive_diagonal == player_id) == 4:
                score += 100
            if np.count_nonzero(positive_diagonal == player_id) == 3:
                score += 7
            if np.count_nonzero(positive_diagonal == player_id) == 2:
                score += 2

    for i in range(3):
        for j in range(4):
            positive_diagonal = np.array(
                [game_field[i, j], game_field[i + 1, j + 1], game_field[i + 2, j + 2], game_field[i + 3, j + 3]])
            if np.count_nonzero(positive_diagonal == player_id) == 4:
                score += 100
            if np.count_nonzero(positive_diagonal == player_id) == 3:
                score += 7
            if np.count_nonzero(positive_diagonal == player_id) == 2:
                score += 2

        if score >= 100:
            result["terminal_node"] = True

        score = score - player_moves
        if player_id == 1:
            result["score"] = -score
        else:
            result["score"] = score

        return result


def get_optimal_move(current_moves, ):
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

        if depth == 2:
            optimal_column = np.argmax(terminal_scores)
            optimal_move = terminal_moves[optimal_column]
            break

    return optimal_column, optimal_move


# print(check_win(moves='001212233344', game_field=game_field))

# player_move = input("Выберите столбец:")
# all_moves.append(player_move)

column, move = get_optimal_move(current_moves=['121'])

...
