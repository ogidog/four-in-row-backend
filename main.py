import numpy as np
import copy

player_id = 1  # 1 - computer, 2 - user
game_fields = np.zeros((6, 7))
all_state = {}


def get_available_row(col, game_fields):
    non_zero_index = np.nonzero(np.array(game_fields[:, col]))[0]
    if len(non_zero_index) == 0:
        return 5
    return non_zero_index[0] - 1


def set_field(col, player_id, game_fields):
    row = get_available_row(col=col, game_fields=game_fields)
    game_fields[row, col] = player_id


def set_states(game_fields, state_key, player_id):
    for col in range(7):
        new_game_fields = copy.deepcopy(game_fields)
        set_field(col=col, player_id=player_id, game_fields=new_game_fields)
        all_state[state_key + str(col)] = new_game_fields


set_states(game_fields=game_fields, state_key="", player_id=player_id)
step = 1
while True:
    all_state_keys = list(filter(lambda item: len(item) == step, copy.deepcopy(list(all_state.keys()))))
    if player_id == 1:
        player_id = 2
    else:
        player_id = 1
    for key in all_state_keys:
        set_states(game_fields=all_state[key], state_key=key, player_id=player_id)

    step += 1

# if col in all_state.keys():
#     all_state[str(col) + str(col)] = new_game_fields
# else:
#     all_state[str(col)] = new_game_fields

# i = 0
# while i < 10:
#     a = input("Input column index:")
#     row_index = get_available_row_index(int(a))
#     print(row_index)
#     if int(row_index) == -1:
#         break
#     i += 1
