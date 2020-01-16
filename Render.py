import copy
import numpy as np
import pygame
import math
from A_star import A_star
from Cube import Cube
from Events import Events


class Render:
    def __init__(self, sw, sh, sl, cam_coords):
        self.SPACE_WIDTH = sw
        self.SPACE_HEIGHT = sh
        self.SPACE_LENGHT = sl
        self.space = np.zeros((self.SPACE_WIDTH, self.SPACE_HEIGHT, self.SPACE_LENGHT), dtype=int)
        self.cubes = self.convert(self.space)
        self.environment = pygame
        self.environment.init()
        self.w = 800
        self.h = 800
        self.cx = self.w // 2
        self.cy = self.h // 2
        self.screen = self.environment.display.set_mode((self.w, self.h))
        self.clock = self.environment.time.Clock()
        self.environment.event.get()
        self.environment.mouse.get_rel()
        self.environment.mouse.set_visible(1)
        self.events = Events(self.environment, self.screen, self.cubes, sw, sh, sl, cam_coords)
        self.current_piece_coords = []
        self.current_piece_cubes = []

    def convert(self, matrix):
        cubes = list()
        for x in range(self.SPACE_WIDTH):
            for y in range(self.SPACE_HEIGHT):
                for z in range(self.SPACE_LENGHT):
                    if matrix[x][y][z] > 0:
                        cubes.append(Cube(matrix[x][y][z] - 1, (x, y, z)))
        return cubes

    def rotate2d(self, pos, rad):
        x, y = pos
        s, c = math.sin(rad), math.cos(rad)
        return x * c - y * s, y * c + x * s

    def get_grid_grid_lines(self):
        lines = list()
        h = self.SPACE_HEIGHT
        for w in range(self.SPACE_WIDTH + 1):
            verts = [(w - 1 / 2, h - 1 / 2, 0 - 1 / 2), (w - 1 / 2, h - 1 / 2, self.SPACE_WIDTH - 1 / 2)]
            lines.append(verts)
        for l in range(self.SPACE_LENGHT + 1):
            verts = [(0 - 1 / 2, h - 1 / 2, l - 1 / 2), (self.SPACE_WIDTH - 1 / 2, h - 1 / 2, l - 1 / 2)]
            lines.append(verts)
        return lines

    def render(self, action, pieces, configuration=0, save_name="none"):
        if action == "show_config":
            self.space = configuration
            self.cubes = self.convert(self.space)
        if action == "add":
            self.space = configuration
            self.cubes = self.convert(self.space)
            self.initial_place_piece(pieces.coords, pieces.color)
        if action == "a_star":
            alg = A_star(self.SPACE_WIDTH, self.SPACE_HEIGHT, self.SPACE_LENGHT, pieces, configuration, self.space)
            alg.start()
            self.cubes = self.convert(self.space)
            self.done_building = False
        if action == "show_piece":
            self.initial_place_piece(pieces.coords, pieces.color)

        grid = self.get_grid_grid_lines()
        done = False
        while not done:
            dt = self.clock.tick() / 1000

            for event in self.environment.event.get():
                self.events.execute_event(event)

            try:
                self.screen.fill((255, 255, 255))
            except:
                break

            if action != "show_piece":
                screen_coords_list = list()
                for line in grid:
                    vert_list, screen_coords = self.get_screen_coords(line)
                    screen_coords_list.append(screen_coords)
                try:
                    for grid_line in screen_coords_list:
                        self.environment.draw.line(self.screen, (0, 0, 0), grid_line[0], grid_line[1])
                except:
                    pass

            face_list = []
            face_color = []
            depth = []
            for obj in self.cubes:
                vert_list, screen_coords = self.get_screen_coords(obj.verts)
                new_face_list, new_face_color, new_depth = self.get_depth(obj, obj.faces, vert_list, screen_coords,
                                                                          "face")
                face_list += new_face_list
                face_color += new_face_color
                depth += new_depth

            edge_list = []
            for obj in self.cubes:
                vert_list, screen_coords = self.get_screen_coords(obj.verts)
                new_edge_list, _, new_depth = self.get_depth(obj, obj.edges, vert_list, screen_coords, "edge")
                edge_list += new_edge_list
                depth += new_depth

            order = sorted((range(len(face_list) + len(edge_list))), key=lambda i: depth[i], reverse=1)

            for i in order:
                try:
                    if i < len(face_list):
                        self.environment.draw.polygon(self.screen, face_color[i], face_list[i])
                    else:
                        self.environment.draw.line(self.screen, (0, 0, 0), edge_list[i - len(face_list)][0],
                                                   edge_list[i - len(face_list)][1])
                except:
                    pass

            self.environment.display.flip()
            key = self.environment.key.get_pressed()
            self.space, self.current_piece_coords, self.current_piece_cubes, done = \
                self.events.update(dt, key, action, save_name, self.space, self.current_piece_coords,
                                   self.current_piece_cubes, done)

            if action == "a_star":
                self.space, self.done_building = alg.get_space()
                self.cubes = self.convert(self.space)

            if done == True:
                return self.space

    def initial_place_piece(self, piece_coords, color):
        self.current_piece_cubes = list()
        for coords in piece_coords:
            self.space[coords[0]][coords[1]][coords[2]] = color
            cube = Cube(color - 1, (coords[0], coords[1], coords[2]))
            self.cubes.append(cube)
            self.current_piece_cubes.append(cube)
        self.current_piece_coords = copy.deepcopy(piece_coords)
        while True:
            new_space, new_current_piece_coords, new_current_piece_cubes = self.events.move_piece(self.space,
                                                                                                  self.current_piece_coords,
                                                                                                  self.current_piece_cubes,
                                                                                                  "down")
            if new_current_piece_coords == self.current_piece_coords and new_current_piece_cubes == self.current_piece_cubes:
                break
            self.current_piece_coords = new_current_piece_coords
            self.current_piece_cubes = new_current_piece_cubes
            self.space = new_space

    def get_screen_coords(self, verts):
        vert_list = []
        screen_coords = []
        for x, y, z in verts:
            x -= self.events.pos[0]
            y -= self.events.pos[1]
            z -= self.events.pos[2]
            x, z = self.rotate2d((x, z), self.events.rot[1])
            y, z = self.rotate2d((y, z), self.events.rot[0])
            vert_list += [(x, y, z)]
            f = 200 / z
            x, y = x * f, y * f
            screen_coords += [(self.cx + int(x), self.cy + int(y))]
        return vert_list, screen_coords

    def get_depth(self, obj, obj_data, vert_list, screen_coords, type):
        face_list = []
        face_color = []
        depth = []
        for f in range(len(obj_data)):
            face = obj_data[f]
            on_screen = False
            for i in face:
                x, y = screen_coords[i]
                if vert_list[i][2] > 0 and 0 < x < self.w and y > 0 and y < self.h:
                    on_screen = True
                    break
            if on_screen:
                coords = [screen_coords[i] for i in face]
                face_list += [coords]
                face_color += [obj.colors[obj.color]]
                if type == "face":
                    depth += [sum(sum(vert_list[j][i] for j in face) ** 2 for i in range(3))]
                if type == "edge":
                    depth += [3.9 * sum(sum(vert_list[j][i] for j in face) ** 2 for i in range(3))]
        return face_list, face_color, depth
