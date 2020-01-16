from threading import Thread
import numpy as np


class A_star(Thread):
    def __init__(self, sw, sh, sl, piece_list, configuration, space):
        super(A_star, self).__init__()
        self.SPACE_WIDTH = sw
        self.SPACE_HEIGHT = sh
        self.SPACE_LENGTH = sl
        self.space = space
        self.piece_list = piece_list
        self.configuration = configuration
        self.min_max_coords()
        self.done = False

    def min_max_coords(self):
        x_min = self.SPACE_WIDTH - 1
        y_min = self.SPACE_HEIGHT - 1
        z_min = self.SPACE_LENGTH - 1
        x_max = 0
        z_max = 0
        for x in range(self.SPACE_WIDTH):
            for y in range(self.SPACE_HEIGHT):
                for z in range(self.SPACE_LENGTH):
                    if self.configuration[x][y][z] > 0:
                        x_min = min(x_min, x)
                        x_max = max(x_max, x)
                        y_min = min(y_min, y)
                        z_min = min(z_min, z)
                        z_max = max(z_max, z)
        self.min_width = x_min
        self.max_width = x_max
        self.min_height = y_min
        self.max_height = self.SPACE_HEIGHT - 1
        self.min_length = z_min
        self.max_length = z_max

    def place_piece(self, x, y, z, piece):
        for coord in piece.coords:
            new_x = x + coord[0]
            new_y = y + coord[1]
            new_z = z + coord[2]
            self.space[new_x][new_y][new_z] = piece.color

    def heuristic(self, w, h, l, piece):
        different_pieces = 0
        number_of_pieces = 0
        flying = True
        li = []
        for coords in piece.coords:
            number_of_pieces += 1
            new_x = w + coords[0]
            new_y = h + coords[1]
            new_z = l + coords[2]
            if not self.valid(new_x, new_y, new_z, self.space):
                return False
            if new_y == self.SPACE_HEIGHT - 1:
                flying = False
            elif new_y > 0 and self.space[new_x][new_y + 1][new_z] != 0 or self.space[new_x][new_y - 1][new_z] != 0:
                flying = False
            if self.configuration[new_x][new_y][new_z] == 0:
                li.append((new_x, new_y, new_z))
                different_pieces += 1
        if flying:
            return False
        return number_of_pieces if different_pieces == 0 else (number_of_pieces - different_pieces) / (
                different_pieces + 1)

    def run(self):
        for i in range(len(self.piece_list)):
            maxim = -1
            w_maxim = -1
            h_maxim = -1
            l_maxim = -1
            piece_maxim = -1
            rotation_maxim = 0
            for piece in self.piece_list:
                for rotation in range(2):
                    for w in range(self.min_width, self.max_width + 1):
                        for h in range(self.min_height, self.max_height + 1):
                            for l in range(self.min_length, self.max_length + 1):
                                value = self.heuristic(w, h, l, piece)
                                if value is False or value < 1:
                                    continue
                                if value > maxim:
                                    maxim = value
                                    w_maxim = w
                                    h_maxim = h
                                    l_maxim = l
                                    piece_maxim = piece
                                    rotation_maxim = rotation
                    piece.rotate()

            if maxim == -1:
                break

            if rotation_maxim == 1:
                piece_maxim.rotate()

            self.place_piece(w_maxim, h_maxim, l_maxim, piece_maxim)
            self.piece_list.remove(piece_maxim)
        self.done = True

    def get_space(self):
        return self.space, self.done

    def valid(self, x, y, z, space):
        if x < 0 or x >= self.SPACE_WIDTH:
            return False
        if y < 0 or y >= self.SPACE_HEIGHT:
            return False
        if z < 0 or z >= self.SPACE_LENGTH:
            return False
        if space[x][y][z] != 0:
            return False
        return True
