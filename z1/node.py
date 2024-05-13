class Node:
    def __init__(self, state, depth=0, parent=None, f=0):
        self.state = state
        self.depth = depth
        self.parent = parent
        self.f = f

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __eq__(self, other):
        return (self.f == other.f) and (self.state == other.state)

    def __ne__(self, other):
        return (self.f != other.f) or (self.state != other.state)
