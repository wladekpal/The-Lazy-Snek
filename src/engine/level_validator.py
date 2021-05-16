MANDATORY_LEVEL_PARTS = ['level_name', 'block_placement', 'block_additional_data', 'snake_data', 'available_blocks']


def check_parts(level_representation):
    try:
        for part in MANDATORY_LEVEL_PARTS:
            level_representation[part]
    except KeyError:
        return False

    return True


def name_not_empty(level_representation):
    return level_representation['level_name'] != ''


def ids_in_range(level_representation):
    board = level_representation['block_placement']
    for line in board:
        for id in line:
            if id < 0 or id > 29:
                return False

    return True


NOT_ENCLOSED_IDS = [0, 2]


def wall_perimeter(level_representation):
    board = level_representation['block_placement']
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] not in NOT_ENCLOSED_IDS:
                if x == 0 or x == len(board)-1:
                    return False
                if y == 0 or y == len(board[x])-1:
                    return False
                if board[x-1][y] == 0 or board[x+1][y] == 0 or board[x][y-1] == 0 or board[x][y+1] == 0:
                    return False

    return True


TELEPORT_BEGIN_ID = 19
TELEPORT_END_ID = 20


def teleports_connected(level_representation):
    board = level_representation['block_placement']
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == TELEPORT_BEGIN_ID:
                additional_data = level_representation['block_additional_data']
                try:
                    field_data = additional_data[x][y]
                    end_y, end_x = tuple(field_data['end_coordinates'])
                    if board[end_x][end_y] != TELEPORT_END_ID:
                        return False
                except (IndexError, KeyError):
                    return False

    return True


VALID_SNAKE_COLORS = ['green', 'red', 'blue']
VALID_SNALE_DIRECTIONS = ['N', 'E', 'S', 'W']


def check_snake_placement(segments):
    if len(segments) < 2:
        return False

    try:
        prev_segment_x, prev_segment_y = tuple(segments[0])
        for segment in segments[1:]:
            cur_segment_x, cur_segment_y = tuple(segment)
            if cur_segment_x == prev_segment_x:
                if abs(cur_segment_y - prev_segment_y) != 1:
                    return False
            elif cur_segment_y == prev_segment_y:
                if abs(cur_segment_x - prev_segment_x) != 1:
                    return False
            else:
                return False

            prev_segment_x, prev_segment_y = cur_segment_x, cur_segment_y
    except IndexError:
        return False

    return True


def check_snakes(level_representation):
    snakes = level_representation['snake_data']

    for snake in snakes:
        try:
            if snake['color'] not in VALID_SNAKE_COLORS:
                return False
            if snake['direction'] not in VALID_SNALE_DIRECTIONS:
                return False
            return check_snake_placement(snake['placement'])
        except KeyError:
            return False
    
    return False


PLACABLE_BLOCKS = [3, 4, 5, 6, 7, 8, 9, 14, 15, 16, 21, 22, 23, 24, 25, 27, 28, 29]


def check_available_blocks(level_representation):
    available_blocks = level_representation['available_blocks']
    for block in available_blocks:
        if block[0] not in PLACABLE_BLOCKS:
            return False

    return True


CONDITIONS = [check_parts, name_not_empty, ids_in_range, wall_perimeter, teleports_connected, check_snakes]


def level_validator(level_representation):
    for condition in CONDITIONS:
        if not condition(level_representation):
            return False

    return True
