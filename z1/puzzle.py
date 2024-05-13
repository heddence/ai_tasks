from copy import deepcopy
from node import Node
from heapq import heappush, heappop


class Puzzle:
    opened = []
    closed = []

    def __init__(self, goal_state, initial_state, size=3):
        self.goal_state = goal_state
        self.initial_state = initial_state
        self.size = size

    def expand_children(self, node):
        """Return list of children nodes.

        :param node: node which represents a state of the puzzle

        :return children: list of children nodes
        """
        children = []
        empty_pos = node.state.index(0)
        if empty_pos - 3 >= 0:  # up state
            child = self.swap(node.state, empty_pos, empty_pos - 3)
            child = Node(child, node.depth + 1, node)
            child.f = self.compute_fn(child)
            children.append(child)
        if empty_pos + 3 < self.size ** 2:  # down state
            child = self.swap(node.state, empty_pos, empty_pos + 3)
            child = Node(child, node.depth + 1, node)
            child.f = self.compute_fn(child)
            children.append(child)
        if empty_pos % 3 != 0:  # left state
            child = self.swap(node.state, empty_pos, empty_pos - 1)
            child = Node(child, node.depth + 1, node)
            child.f = self.compute_fn(child)
            children.append(child)
        if (empty_pos + 1) % 3 != 0:  # right state
            child = self.swap(node.state, empty_pos, empty_pos + 1)
            child = Node(child, node.depth + 1, node)
            child.f = self.compute_fn(child)
            children.append(child)
        return children

    def solve_puzzle(self):
        """Solve puzzle using A* algorithm."""
        initial_node = Node(self.initial_state)                       # create node from an initial_state
        initial_node.f = self.compute_fn(initial_node)                # compute heuristic function of an initial_state
        heappush(self.opened, (initial_node.f, initial_node))  # push initial node to PriorityQueue

        while self.opened:
            node = heappop(self.opened)[1]                            # pop element from PriorityQueue

            if node.depth == 20:
                print('Not solvable')
                break

            if node.state == self.goal_state:                         # check if current node state == goal state
                self.print_puzzle(node)                               # print puzzle
                print('Done!')
                break

            children = self.expand_children(node)                     # get list of all children from a current node
            for child in children:
                if (child.f, child) not in self.closed:               # check if child has not been seen
                    heappush(self.opened, (child.f, child))    # add children to opened PriorityQueue
            heappush(self.closed, (node.f, node))              # add parent to closed PriorityQueue

    def compute_fn(self, node):
        """Compute cost function.

        :param node: node on which cost function are computed

        :return f: cost function of a node
        """
        return node.depth + self.compute_h2(node.state)  # compute f function as depth + heuristic

    def compute_h1(self, state):
        """Compute heuristic function 1 (Number of wrong positions).

        :param state: state of a node

        :return h1: heuristic function 1
        """
        h1 = 0
        for i, j in zip(state, self.goal_state):
            if i != j:
                h1 += 1
        return h1

    def compute_h2(self, state):
        """Compute heuristic function 2 (Euclidian distance).

        :param state: state of a node

        :return h1: heuristic function 2
        """
        h2 = 0
        for i, j in zip(state, self.goal_state):
            h2 += abs(j - i)
        return h2

    def print_puzzle(self, node):
        if node.parent is None:
            self.print_node(node)
        else:
            self.print_puzzle(node.parent)
            self.print_node(node)

    def print_node(self, node):
        for first, second, third in zip(
                node.state[::self.size],
                node.state[1::self.size],
                node.state[2::self.size]):
            print(f'| {first} | {second} | {third} |')
        print(f'Depth: {node.depth} | f: {node.f}')
        print()

    @staticmethod
    def swap(state, i, j):
        """Return child_state from the parent state.

        :param i: first index in a list
        :param j: second index in a list

        :return child_state: list representing the state of a child
        """
        child_state = deepcopy(state)
        child_state[i], child_state[j] = child_state[j], child_state[i]
        return child_state
