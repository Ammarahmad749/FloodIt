import math
import cv2
import numpy as np


class board():
    color_set = set()
    color_val = {}
    matrix = []
    graph = {}

    def set_graph(self):
        '''
        create a graph for board (graphical representation of board)
        '''
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[x])):
                index = (x, y)
                childs = self.get_childs(x, y)
                self.graph[index] = childs
        return self.graph

    def set_board(self, image):
        '''
        set the board image into 2D array
        '''
        edg = self.get_edges(image)
        min_col, min_row = self.get_min_x_and_y(edg)
        row = np.int0(min_row/2)
        while row < image.shape[0]:
            column = []
            col = np.int0(min_col/2)
            count_x = 0
            while col < image.shape[1]:
                color = image[row, col]
                color = (color[2], color[1], color[0])
                hex_col = self.get_color(color)
                col_val = self.get_color_val(hex_col)
                column.append(col_val)
                col = col+min_col
                count_x += 1
            self.matrix.append(column)
            row = row+min_row
        return self.matrix

    def get_color(self, color):
        '''
        get the color value in hex of RGB of a pixel
        '''
        add_to_set = True
        if color not in self.color_set:
            for col in self.color_set:
                # caluculate the distance of color inorder to identify the similarity
                distance = math.sqrt(sum([math.pow(int(col[0])-int(color[0]), 2),
                                         math.pow(int(col[1])-int(color[1]), 2),
                                         math.pow(int(col[2])-int(color[2]), 2)]))
                if distance < 10:
                    color = col
                    add_to_set = False
                    break
        if add_to_set:
            self.color_set.add(color)

        return '#%02x%02x%02x' % color

    def get_color_val(self, color):
        '''
        Assigning value to a color (Key store in color_val dict)
        '''
        try:
            self.color_val[color]
        except KeyError:
            self.color_val[color] = len(self.color_val.keys())

        return self.color_val[color]

    def get_edges(self, image):
        '''
        getting all edges of the board image
        '''
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = np.float32(gray)
        corners = cv2.goodFeaturesToTrack(gray, 200, 0.01, 10)
        corners = np.int0(corners)
        edge_list = []
        for corner in corners:
            x, y = corner.ravel()
            edge_list.append((x, y))

        return edge_list

    def get_childs(self, x, y):
        '''
        getting childs of a single  boxfor graph
        '''
        child_right = self.get_right_child(x, y)
        child_left = self.get_left_child(x, y)
        childs = set()
        if child_right:
            childs.add(child_right)
        if child_left:
            childs.add(child_left)

        return childs

    def get_right_child(self, x, y):
        '''
        get right child x, y+1
        '''
        try:
            child = self.matrix[x][y+1]
        except Exception:
            child = None
        if child is not None:
            child = (x, y+1)
        return child

    def get_left_child(self, x, y):
        '''
        get left child x+1, y
        '''
        try:
            child = self.matrix[x+1][y]
        except Exception:
            child = None
        if child is not None:
            child = (x+1, y)
        return child

    def get_min_x_and_y(self, edge_list):
        '''
        get the reference point to determin minium height and width of a box
        in grid
        '''
        x_arr, y_arr = self.get_x_y_list(edge_list)
        x_arr = np.array(sorted(x_arr))
        y_arr = np.array(sorted(y_arr))
        x_arr = list(filter(lambda a: a > 10, np.diff(x_arr)))
        y_arr = list(filter(lambda a: a > 10, np.diff(y_arr)))
        return max(x_arr), max(y_arr)

    def get_x_y_list(self, edge_list):
        '''
        return list of x and y cordinate of all edges detected
        '''
        x = [x[0] for x in edge_list]
        y = [y[1] for y in edge_list]
        return x, y

    def make_board(self, image):
        '''
        main function to set board
        '''
        img = cv2.imread(image)
        self.set_board(img)
        self.set_graph()

        return self.matrix, self.graph, self.color_val


# cv2.imshow('Corner', img)
# cv2.waitKey()
