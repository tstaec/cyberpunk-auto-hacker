# Credit for this: Nicholas Swift
# as found at https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
# Credit to Ryan Collingwood for the fixes https://gist.github.com/ryancollingwood/32446307e976a11a1185a5394d6657bc
from enum import Enum, IntEnum
from warnings import warn
import heapq


class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent=None, position=None, code=None, row_type=None):
        self.parent = parent
        self.position = position
        self.code = code
        self.row_type = row_type

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __repr__(self):
        return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
        return self.f < other.f

    # defining greater than for purposes of heap queue
    def __gt__(self, other):
        return self.f > other.f


def find_path(matrix, end_paths, max_path_length):
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    :param matrix:
    :param end_paths:
    :param max_path_length:
    :param start:
    :return:
    """

    # Initialize open list
    open_list = []

    # Heapify the open_list and Add the start nodes
    heapq.heapify(open_list)
    start_nodes = create_nodes(Node(None, [0, 0], None), RowType.Row, matrix[0, :], end_paths, False)
    for start_node in start_nodes:
        heapq.heappush(open_list, start_node)

    # Adding a stop condition
    outer_iterations = 0
    max_iterations = len(matrix) ** 10

    # Loop until you find the end
    while len(open_list) > 0:
        outer_iterations += 1

        if outer_iterations > max_iterations:
            # if we hit this point return the path such as it is
            # it will not contain the destination
            warn("giving up on pathfinding too many iterations")
            return return_path(current_node)

            # Get the current node
        current_node = heapq.heappop(open_list)

        # Check if we found the goal
        if is_completed(current_node, end_paths):
            print('Completed path found')
            return return_path(current_node)

        # check if the current path is longer than the max path length
        # todo ensure that best node is returned if no complete solution ist found
        if len(return_path_code(current_node)) >= max_path_length * 2:
            continue

        # Generate children
        children = []

        next_nodes = get_nodes(current_node, matrix, end_paths)
        for new_node in next_nodes:

            # Make sure node does not already exist in path
            #todo check coordinates

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Add the child to the open list
            heapq.heappush(open_list, child)

    warn("Couldn't get a path to destination")
    return None


def is_completed(node, end_paths):
    path = return_path_code(node)
    return all(end_path in path for end_path in end_paths)


def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path


def return_path_code(current_node):
    path = []
    current = current_node
    while current is not None and current.code is not None:
        path.append(current.code)
        current = current.parent
    return ''.join(path[::-1])  # Return reversed path


def get_nodes(current_node, matrix, end_paths):
    row_type = current_node.row_type * -1  # invert the row type for child nodes
    if row_type == RowType.Row:
        row_elements = matrix[current_node.position[1], :]
    else:
        row_elements = matrix[:, current_node.position[0]]

    return create_nodes(current_node, row_type, row_elements, end_paths)


def create_nodes(current_node, row_type, row_elements, end_paths, exclude_parent=True):
    nodes = []
    i = 0
    for element in row_elements:
        if row_type == RowType.Row:
            position = [i, current_node.position[1]]
        else:
            position = [current_node.position[0], i]
        i += 1

        # Null the parent node if the current node is the node we had to create to feed the first row
        parent_node = current_node
        if current_node.position == [0, 0] and current_node.code is None:
            parent_node = None

        new_node = Node(parent_node, position, element, row_type)
        if exclude_parent and new_node == current_node:
            continue
        nodes.append(new_node)
        new_node.f = get_path_value(new_node, end_paths)

    return nodes


def get_path_value(node, end_paths):
    value = 0
    i = 0
    path = return_path_code(node)

    # Ensure that paths that solve one or more required sequences are valued higher
    for end_path in end_paths:
        i += 1
        if end_path in path:
            value += 1000 * i
            continue

        # Check for the path so solve an required sequence partially
        # split the end_path by the codes
        partial_paths = [end_path[i:i + 2] for i in range(0, len(end_path), 2)]
        aggregated_path = ''
        for partial_path in partial_paths:
            aggregated_path += partial_path
            # Check if tha current path ends with a part of an required path
            if path.endswith(aggregated_path):
                value += len(aggregated_path)

    return value * -1  # invert value so min value queue can be used


class RowType(IntEnum):
    Row = -1
    Column = 1
