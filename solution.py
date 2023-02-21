import copy
import numpy as np

class Flood_it:
    def __init__(self, matrix):
        self.matrix = matrix
        self.rows, self.columns = np.shape(matrix)
        self.colors = 6

    def neighbours(self, points, return_value):
        values = points.pop()
        return_value.add(values)
        x = values[0]
        y = values[1]
        return [(x, y+1), (x, y-1), (x+1, y), (x-1, y)]

    def max_points(self, x, y):
        values = set()
        check = self.matrix[x][y]
        stack = []
        stack.append((x, y))
        while len(stack) > 0:
            adj_indexes = self.neighbours(stack, values)

            for elem in adj_indexes:
                if not (elem in values):
                    if elem[0] < self.rows and elem[0] >= 0 and elem[1] < self.columns and elem[1] >= 0:
                        if self.matrix[elem[0]][elem[1]] == check:
                            stack.append(elem)

        return values

    def flood_it(self, x, y, c):
        cord = self.max_points(x, y)
        # print("cord",cord)
        for i in cord:
            self.matrix[i[0]][i[1]] = c

    def solve(self):

        deep_copy = copy.deepcopy(self)
        check = self.max_points(0, 0)
        step_values = []
        path_length = []
        moves = []
        moved_matrix = copy.deepcopy(self.matrix)
        count = 1

        while len(check) != (self.rows*self.columns):
            colored_copies = []
            for i in range(0, self.colors):
                path_length.append(0)
            for i in range(0, self.colors):
                colored_copies.append(copy.deepcopy(deep_copy))
            for i in range(0, self.colors):
                colored_copies[i].flood_it(0, 0, i)
                moves = colored_copies[i].max_points(0, 0)
                path_length[i] = len(moves)
            max_index = path_length.index(np.max(path_length))
            # print(colored_copies[max_index].rows)
            print("\t\tStep", count, " : Choosing ",
                  max_index, "as our move\n")
            for i in moves:
                moved_matrix[i[0]][i[1]] = max_index
            for row in moved_matrix:
                print([str(x) for x in row], "\n")

            deep_copy = colored_copies[max_index]
            check = deep_copy.max_points(0, 0)
            # if(len(check)==16):
            #     print(check)
            step_values.append(max_index)
            count = count+1
        return step_values
