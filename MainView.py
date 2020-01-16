import random
import tkinter as tk
import Pieces
from Render import Render
from tkinter import messagebox


class MainView(tk.Frame):
    def __init__(self, root, data):
        tk.Frame.__init__(self, root)
        self.data = data

    def startAlg(self):
        # validation
        if len(self.data.selected_conf_maxtrix) == 0:
            messagebox.showwarning("Warning", "Please select configuration")
            return 0

        bool = False
        for i in self.data.piecesToUse:
            if self.data.piecesToUse[i] != 0:
                bool = True
                break

        if bool == False:
            messagebox.showwarning("Warning", "Please select pieces")
            return 0

        listofPieces = list()
        for contor in self.data.piecesToUse.keys():
            for i in range(self.data.piecesToUse[contor]):
                listofPieces.append(Pieces.Piece(Pieces.pieces[contor], random.randint(0, 6)))

        render = Render(self.data.SPACE_WIDTH, self.data.SPACE_HEIGHT, self.data.SPACE_LENGTH, (7,6,-8))
        render.render("a_star", listofPieces, self.data.selected_conf_maxtrix)

    def showConfig(self):
        if len(self.data.selected_conf_maxtrix) == 0:
            messagebox.showwarning("Warning", "Please select configuration")
            return 0

        render = Render(self.data.SPACE_WIDTH, self.data.SPACE_HEIGHT, self.data.SPACE_LENGTH, (7,6,-8))
        render.render("show_config", [], self.data.selected_conf_maxtrix)

    def page3_switch(self):
        self.data.page2.getVals()
        self.data.page3.readConfFromFile()
        self.data.page3.showConf()
        self.data.page3.tkraise()

