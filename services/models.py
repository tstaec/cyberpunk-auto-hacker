from enum import IntEnum


class Node:
    def __init__(self, parent=None, position=None, code=None, row_type=None):
        self.parent = parent
        self.position = position
        self.code = code
        self.row_type = row_type

        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __repr__(self):
        return f"{self.position} - {self.code} - f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
        return self.f < other.f

    # defining greater than for purposes of heap queue
    def __gt__(self, other):
        return self.f > other.f


class OcrResult:
    def __init__(self, code=None, position=None):
        self.position = position
        self.code = code


class RowType(IntEnum):
    Row = -1
    Column = 1