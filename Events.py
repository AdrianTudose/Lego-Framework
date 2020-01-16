import copy
import math
import sys


class Events:
    def __init__(self, pygame, screen, cubes, sw, sh, sl, pos=(0, 0, 0), rot=(0, 0)):
        self.SPACE_WIDTH = sw
        self.SPACE_HEIGHT = sh
        self.SPACE_LENGTH = sl
        self.environment = pygame
        self.screen = screen
        self.cubes = cubes
        self.pos = list(pos)
        self.rot = list(rot)
        self.mouse_rotate = False
        self.MOVE_DIRECTIONS = {"down": [0, 1, 0], "up": [0, -1, 0], "right": [1, 0, 0], "left": [-1, 0, 0],
                                "forward": [0, 0, 1], "backward": [0, 0, -1]}
        self.key_pressed = False

    def execute_event(self, event):
        if event.type == self.environment.QUIT:
            self.environment.quit()
        if event.type == self.environment.MOUSEBUTTONDOWN:
            self.mouse_rotate = True
        if event.type == self.environment.MOUSEBUTTONUP:
            self.mouse_rotate = False
        if event.type == self.environment.MOUSEMOTION and self.mouse_rotate == True:
            x, y = event.rel
            x /= 200
            y /= 200
            self.rot[0] += y
            self.rot[1] += x

    def update(self, dt, key, action, save_name, space, coords, cubes, done):
        s = dt * 10
        x, y = s * math.sin(self.rot[1]), s * math.cos(self.rot[1])
        if key[self.environment.K_e]:
            self.pos[1] += s
        elif key[self.environment.K_q]:
            self.pos[1] -= s
        elif key[self.environment.K_w]:
            self.pos[2] += y
            self.pos[0] += x
        elif key[self.environment.K_s]:
            self.pos[2] -= y
            self.pos[0] -= x
        elif key[self.environment.K_d]:
            self.pos[0] += y
            self.pos[2] -= x
        elif key[self.environment.K_a]:
            self.pos[0] -= y
            self.pos[2] += x
        if action == "add":
            if key[self.environment.K_LEFT]:
                if self.key_pressed == False:
                    space, coords, cubes = self.move_piece(space, coords, cubes, "left")
                self.key_pressed = True
            elif key[self.environment.K_RIGHT]:
                if self.key_pressed == False:
                    space, coords, cubes = self.move_piece(space, coords, cubes, "right")
                self.key_pressed = True
            elif key[self.environment.K_UP]:
                if self.key_pressed == False:
                    space, coords, cubes = self.move_piece(space, coords, cubes, "forward")
                self.key_pressed = True
            elif key[self.environment.K_DOWN]:
                if self.key_pressed == False:
                    space, coords, cubes = self.move_piece(space, coords, cubes, "backward")
                self.key_pressed = True
            elif key[self.environment.K_KP_PLUS]:
                if self.key_pressed == False:
                    space, coords, cubes = self.move_piece(space, coords, cubes, "up")
                self.key_pressed = True
            elif key[self.environment.K_KP_MINUS]:
                if self.key_pressed == False:
                    space, coords, cubes = self.move_piece(space, coords, cubes, "down")
                self.key_pressed = True
            elif key[self.environment.K_KP_MULTIPLY]:
                if self.key_pressed == False:
                    space, coords, cubes = self.move_piece(space, coords, cubes, "rotate")
                self.key_pressed = True
            elif key[self.environment.K_SPACE]:
                if self.key_pressed == False and not self.flying(space, coords):
                    done = True
                    self.save_screen_shot(save_name)
                    self.environment.quit()
                self.key_pressed = True
            elif key[self.environment.K_ESCAPE]:
                if self.key_pressed == False:
                    done = True
                    space = self.remove_piece(space, coords)
                    self.environment.quit()
                self.key_pressed = True
            else:
                self.key_pressed = False
        return space, coords, cubes, done

    def get_new_coords(self, pieces_coords, move_type):
        if move_type == "rotate":
            min_width = min([x for x, y, z in pieces_coords])
            min_length = min([z for x, y, z in pieces_coords])

            new_piece_coords = copy.deepcopy(pieces_coords)

            for i in range(len(pieces_coords)):
                new_piece_coords[i][0], new_piece_coords[i][2] = \
                    new_piece_coords[i][2] - min_length + min_width, \
                    new_piece_coords[i][0] - min_width + min_length
        else:
            move_width = self.MOVE_DIRECTIONS[move_type][0]
            move_height = self.MOVE_DIRECTIONS[move_type][1]
            move_length = self.MOVE_DIRECTIONS[move_type][2]

            new_piece_coords = copy.deepcopy(pieces_coords)

            for i in range(len(pieces_coords)):
                new_piece_coords[i][0] += move_width
                new_piece_coords[i][1] += move_height
                new_piece_coords[i][2] += move_length

        return new_piece_coords

    def move_piece(self, space, pieces_coords, piece_cubes, move_type):
        color = space[pieces_coords[0][0]][pieces_coords[0][1]][pieces_coords[0][2]]
        new_pieces_coords = self.get_new_coords(pieces_coords, move_type)
        if self.valid(space, pieces_coords, new_pieces_coords) == False:
            return space, pieces_coords, piece_cubes
        for piece in pieces_coords:
            space[piece[0]][piece[1]][piece[2]] = 0
        for i, cube in enumerate(piece_cubes):
            cube.new_coords(new_pieces_coords[i][0], new_pieces_coords[i][1], new_pieces_coords[i][2])
        for piece in new_pieces_coords:
            space[piece[0]][piece[1]][piece[2]] = color
        return space, new_pieces_coords, piece_cubes

    def valid(self, space, old_coords, new_coords):
        for coords in new_coords:
            x = coords[0]
            y = coords[1]
            z = coords[2]
            if x < 0 or x >= self.SPACE_WIDTH:
                return False
            if y < 0 or y >= self.SPACE_HEIGHT:
                return False
            if z < 0 or z >= self.SPACE_LENGTH:
                return False
            if [x, y, z] not in old_coords and space[x][y][z] != 0:
                return False
        return True

    def flying(self, space, coords):
        min_height = max([y for x, y, z in coords])
        max_height = min([y for x, y, z in coords])
        if min_height == self.SPACE_HEIGHT - 1:
            return False
        for coord in coords:
            if coord[1] == min_height:
                if space[coord[0], coord[1] + 1, coord[2]] != 0:
                    return False
            if max_height > 0 and coord[1] == max_height:
                if space[coord[0], coord[1] - 1, coord[2]] != 0:
                    return False
        return True

    def save_screen_shot(self, save_name):
        self.environment.image.save(self.screen, "images\\configuratii\\" + save_name + ".png")

    def remove_piece(self, space, pieces_coords):
        for piece in pieces_coords:
            space[piece[0]][piece[1]][piece[2]] = 0
        return space
