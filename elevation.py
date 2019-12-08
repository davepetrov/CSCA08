"""Assignment 2 functions."""

from typing import List


THREE_BY_THREE = [[1, 2, 1],
                  [4, 6, 5],
                  [7, 8, 9]]

FOUR_BY_FOUR = [[1, 2, 6, 5],
                [4, 5, 3, 2],
                [7, 9, 8, 1],
                [1, 2, 1, 4]]

UNIQUE_3X3 = [[1, 2, 3],
              [9, 8, 7],
              [4, 5, 6]]

UNIQUE_4X4 = [[10, 2, 3, 30],
              [9, 8, 7, 11],
              [4, 5, 6, 12],
              [13, 14, 15, 16]]


def get_surrounded_map(elevation_map: List[List[int]]) -> list:
    """
    Return new elevation map surrounded by None Type
    placeholders on the North, South, East, West side of elevation_map

     Precondition: elevation_map is a valid elevation map.
                  0 <= map_row < len(elevation_map).
    
    >> get_surrounded_map([[8]])
    [[None, None, None], [None, 8, None], [None, None, None]]
    
    """

    new_map = [[None] * (len(elevation_map) + 2)]
    for row in range(len(elevation_map)):
        new_map.append([None])
        for col in range(len(elevation_map)):
            new_map[row + 1].append(elevation_map[row][col])
        new_map[row + 1].append(None)
    new_map.append([None] * (len(elevation_map) + 2))

    return new_map


def compare_elevations_within_row(elevation_map: List[List[int]], map_row: int,
                                  level: int) -> List[int]:
    """Return a new list containing the three counts: the number of
    elevations from row number map_row of elevation map elevation_map
    that are less than, equal to, and greater than elevation level.

    Precondition: elevation_map is a valid elevation map.
                  0 <= map_row < len(elevation_map).

    >>> compare_elevations_within_row(THREE_BY_THREE, 1, 5)
    [1, 1, 1]
    >>> compare_elevations_within_row(FOUR_BY_FOUR, 1, 2)
    [0, 1, 3]

    """

    count_less_than = 0
    count_equal_to = 0
    count_greater_than = 0

    for col in range(len(elevation_map)):
        if elevation_map[map_row][col] < level:
            count_less_than += 1
        elif elevation_map[map_row][col] > level:
            count_greater_than += 1
        else:
            count_equal_to += 1

    return [count_less_than, count_equal_to, count_greater_than]


def update_elevation(elevation_map: List[List[int]], start: List[int],
                     stop: List[int], delta: int) -> None:
    """Modify elevation map elevation_map so that the elevation of each
    cell between cells start and stop, inclusive, changes by amount
    delta.

    Precondition: elevation_map is a valid elevation map.
                  start and stop are valid cells in elevation_map.
                  start and stop are in the same row or column or both.
                  If start and stop are in the same row,
                      start's column <=  stop's column.
                  If start and stop are in the same column,
                      start's row <=  stop's row.
                  elevation_map[i, j] + delta >= 1
                      for each cell [i, j] that will change.

    >>> THREE_BY_THREE_COPY = [[1, 2, 1],
    ...                        [4, 6, 5],
    ...                        [7, 8, 9]]
    >>> update_elevation(THREE_BY_THREE_COPY, [1, 0], [1, 1], -2)
    >>> THREE_BY_THREE_COPY
    [[1, 2, 1], [2, 4, 5], [7, 8, 9]]
    >>> FOUR_BY_FOUR_COPY = [[1, 2, 6, 5],
    ...                      [4, 5, 3, 2],
    ...                      [7, 9, 8, 1],
    ...                      [1, 2, 1, 4]]
    >>> update_elevation(FOUR_BY_FOUR_COPY, [1, 2], [3, 2], 1)
    >>> FOUR_BY_FOUR_COPY
    [[1, 2, 6, 5], [4, 5, 4, 2], [7, 9, 9, 1], [1, 2, 2, 4]]

    """
    start_col = start[1]
    start_row = start[0]
    stop_col = stop[1]
    stop_row = stop[0]
    if start_col == stop_col and start_row != stop_row:
        for i in range(start_row, stop_row + 1):
            elevation_map[i][start_col] += delta

    elif start_col != stop_col and start_row == stop_row:
        for i in range(start_col, stop_col + 1):
            elevation_map[start_row][i] += delta
    else:
        elevation_map[start_row][stop_col] += delta


def get_average_elevation(elevation_map: List[List[int]]) -> float:
    """Return the average elevation across all cells in the elevation map
    elevation_map.

    Precondition: elevation_map is a valid elevation map.

    #>>> get_average_elevation(UNIQUE_3X3)
    5.0
    >>> get_average_elevation(FOUR_BY_FOUR)
    3.8125
    """
    total_sum = 0
    total_values = len(elevation_map)**2
    for row in elevation_map:
        for val in row:
            total_sum += val
    return total_sum / total_values


def find_peak(elevation_map: List[List[int]]) -> List[int]:
    """Return the cell that is the highest point in the elevation map
    elevation_map.

    Precondition: elevation_map is a valid elevation map.
                  Every elevation value in elevation_map is unique.

    >>> find_peak(UNIQUE_3X3)
    [1, 0]
    >>> find_peak(UNIQUE_4X4)
    [0, 3]
    """
    highest_value = 0
    highest_cell = None
    for row in range(len(elevation_map)):
        for col in range(len(elevation_map)):
            if elevation_map[row][col] > highest_value:
                highest_cell = [row, col]
                highest_value = elevation_map[row][col]
    return highest_cell


def is_sink(elevation_map: List[List[int]], cell: List[int]) -> bool:
    """Return True if and only if cell exists in the elevation map
    elevation_map and cell is a sink.

    Precondition: elevation_map is a valid elevation map.
                  cell is a 2-element list.

    >>> is_sink(THREE_BY_THREE, [0, 5])
    False
    >>> is_sink(THREE_BY_THREE, [0, 2])
    True
    >>> is_sink(THREE_BY_THREE, [1, 1])
    False
    >>> is_sink(FOUR_BY_FOUR, [2, 3])
    True
    >>> is_sink(FOUR_BY_FOUR, [3, 2])
    True
    >>> is_sink(FOUR_BY_FOUR, [1, 3])
    False
    """
    cell_col = cell[1]
    cell_row = cell[0]
    if 0 <= cell_row <= len(elevation_map) - 1 and \
            0 <= cell_col <= len(elevation_map) - 1:
        adj_cells_vals_inclusive = []
        new_map = get_surrounded_map(elevation_map)
        for row in range(-1, 2):
            for col in range(-1, 2):
                if new_map[cell_row + 1 + row][cell_col + 1 + col] is not None:
                    next_row = cell_row + 1 + row
                    next_col = cell_col + 1 + col
                    adj_cells_vals_inclusive.append(new_map[next_row][next_col])

        cell_value = elevation_map[cell_row][cell_col]
        return cell_value == min(adj_cells_vals_inclusive)
    return False


def find_local_sink(elevation_map: List[List[int]],
                    cell: List[int]) -> List[int]:
    """Return the local sink of cell cell in elevation map elevation_map.

    Precondition: elevation_map is a valid elevation map.
                  elevation_map contains no duplicate elevation values.
                  cell is a valid cell in elevation_map.

    >>> find_local_sink(UNIQUE_3X3, [1, 1])
    [0, 0]
    >>> find_local_sink(UNIQUE_3X3, [2, 0])
    [2, 0]
    >>> find_local_sink(UNIQUE_4X4, [1, 3])
    [0, 2]
    >>> find_local_sink(UNIQUE_4X4, [2, 2])
    [2, 1]
    """
    cell_row = cell[0]
    cell_col = cell[1]

    new_map = get_surrounded_map(elevation_map)

    min_cell_val = elevation_map[cell_row][cell_col]
    min_cell_row = cell_row
    min_cell_col = cell_col
    for row in range(-1, 2):
        for col in range(-1, 2):
            current_cell_val = new_map[cell_row + 1 + row][cell_col + 1 + col]
            if current_cell_val is not None:
                if current_cell_val <= min_cell_val:
                    min_cell_val = current_cell_val
                    min_cell_row = cell_row + row
                    min_cell_col = cell_col + col

    return [min_cell_row, min_cell_col]


def can_hike_to(elevation_map: List[List[int]], start: List[int],
                dest: List[int], supplies: int) -> bool:
    """Return True if and only if a hiker can go from start to dest in
    elevation_map without running out of supplies.

    Precondition: elevation_map is a valid elevation map.
                  start and dest are valid cells in elevation_map.
                  dest is North-West of start.
                  supplies >= 0

    >>> map = [[1, 6, 5, 6],
    ...        [2, 5, 6, 8],
    ...        [7, 2, 8, 1],
    ...        [4, 4, 7, 3]]
    >>> can_hike_to(map, [3, 3], [2, 2], 10)
    True
    >>> can_hike_to(map, [3, 3], [2, 2], 8)
    False
    >>> can_hike_to(map, [3, 3], [3, 0], 7)
    True
    >>> can_hike_to(map, [3, 3], [3, 0], 6)
    False
    >>> can_hike_to(map, [3, 3], [0, 0], 18)
    True
    >>> can_hike_to(map, [3, 3], [0, 0], 17)
    False                                                                                                

    """
    dest_col = dest[1]
    dest_row = dest[0]
    current_col = start[1]
    current_row = start[0]
    current_val = elevation_map[current_row][current_col]

    while supplies >= 0:
        if current_row == dest_row and current_col == dest_col:
            return True

        current_val = elevation_map[current_row][current_col]
        north_val = elevation_map[current_row - 1][current_col]
        west_val = elevation_map[current_row][current_col - 1]
        west_diff = abs(west_val - current_val)
        north_diff = abs(north_val - current_val)
        if (dest_col == current_col or dest_row < current_row)and \
        north_diff <= west_diff:
            current_row -= 1
            supplies -= north_diff
        else:
            current_col -= 1
            supplies -= west_diff

    return False

def make_map_even(elevation_map: List[List[int]]) -> List[List[int]]:
    """
    Modify make_map_even such that add another colomn of cells at the 
    end of each row of the same value in the last colomn of the original
    elevation map, and add another row of cells of the same value in the 
    last row of the original elevation map
    
    Precondition: elevation_map is a valid elevation map. 
                           len(elevation_map) % 2 != 0
                           
    >>> make_map_even(
    ...     [[7, 9, 1],
    ...      [4, 2, 1],
    ...      [3, 2, 3]])
    [[7, 9, 1, 1], [4, 2, 1, 1], [3, 2, 3, 3], [3, 2, 3, 3]]
    
    >>> make_map_even([[7]])
    [[7, 7], [7, 7]]
    """
    for i in range(len(elevation_map)):
        for j in range(len(elevation_map)):
            if i <= len(elevation_map) - 1 and j == len(elevation_map) - 1:
                elevation_map[i].append(elevation_map[i][-1])
    elevation_map.append([])
    for j in range(len(elevation_map)):
        elevation_map[-1].append(elevation_map[-2][j])    
        

def get_lower_resolution(elevation_map: List[List[int]]) -> List[List[int]]:
    """Return a new elevation map, which is constructed from the values
    of elevation_map by decreasing the number of elevation points
    within it.

    Precondition: elevation_map is a valid elevation map.

    >>> get_lower_resolution(
    ...     [[1, 6, 5, 6],
    ...      [2, 5, 6, 8],
    ...      [7, 2, 8, 1],
    ...      [4, 4, 7, 3]])
    [[3, 6], [4, 4]]
    >>> get_lower_resolution(
    ...     [[7, 9, 1],
    ...      [4, 2, 1],
    ...      [3, 2, 3]])
    [[5, 1], [2, 3]]

    """
    if len(elevation_map) % 2 != 0:
        make_map_even(elevation_map)

    new_elevation_map = []
    for row in range(len(elevation_map) // 2):
        new_elevation_map.append([])
        for col in range(len(elevation_map) // 2):
            new_elevation_map[row].append(0)

    for i in range(len(elevation_map) // 2):
        for j in range(len(elevation_map) // 2):
            total = 0
            for row in range(2):
                for col in range(2):
                    curent_cell_val = elevation_map[i * 2 + row][j * 2 + col] 
                    total += curent_cell_val
            new_elevation_map[i][j] = total // 4

    return new_elevation_map
