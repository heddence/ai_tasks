from puzzle import Puzzle

if __name__ == '__main__':
    initial_state = [int(item) for item in input('Enter the initial_state (space-separated): ').split()]
    goal_state = [int(item) for item in input('Enter the goal_state (space-separated): ').split()]
    size = int(input('Enter the size of the puzzle: '))

    puzzle = Puzzle(goal_state, initial_state, size)
    puzzle.solve_puzzle()
