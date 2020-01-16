import pickle
from Page import Page
import tkinter as tk


# from PIL import Image

class Page3(Page):
    def __init__(self, mainPage, data):
        Page.__init__(self, mainPage)
        self.data = data
        self.configure(bg="#fcdfc7")

        photo = tk.PhotoImage(file=r"images\b4.png")
        w = tk.Label(self, image=photo)
        w.place(x=0, y=0, relwidth=1, relheight=1)
        w.image = photo

        # read conf from file
        self.configs = dict()
        self.readConfFromFile()

        self.labels = []
        self.buttons = []

        canvasConfig = tk.Canvas(self)
        canvasConfig.pack(side=tk.LEFT, fill='both', padx=100, expand=True)
        scroll = tk.Scrollbar(self, orient=tk.VERTICAL, command=canvasConfig.yview)
        scroll.pack(side=tk.RIGHT, fill='y')
        self.scrollable_frame = tk.Frame(canvasConfig)
        self.scrollable_frame.bind("<Configure>", lambda e: canvasConfig.configure(scrollregion=canvasConfig.bbox("all")))
        self.scrollable_frame.configure(bg="#d5e8d8")
        canvasConfig.create_window(0, 0, window=self.scrollable_frame, anchor='nw')
        canvasConfig.configure(bg="#d5e8d8")
        self.conf = tk.IntVar()

        canvasConfig.config(yscrollcommand=scroll.set)

        canvasConfig.pack()
        delete = tk.Button(self, text="Delete", command=self.deleteConf, width=8, height=1,
                           background='#b2ebe3',
                           font='Arial').place(x=685, y=170)

    def setConfig(self, arg):
        self.data.selected_conf_maxtrix = self.configs[arg]
        self.data.selected_conf_name = arg



    def readConfFromFile(self):
        with open('ConfigurationsList.bin', 'rb') as f:
            data_loaded = pickle.load(f)
        self.configs.clear()
        for i in data_loaded:
            self.configs[i.name] = i.coords

    def showConf(self):
        for label in self.labels:
            label.pack_forget()
        for button in self.buttons:
            button.pack_forget()

        self.labels.clear()
        self.buttons.clear()

        for i in self.configs.keys():
            photo = tk.PhotoImage(file=r"images\configuratii\{}.PNG".format(i))
            photo = photo.subsample(2,2)

            w = tk.Label(self.scrollable_frame, image=photo)
            w.pack(anchor='n', padx=120, pady=7, expand=True)
            w.image = photo
            button = tk.Radiobutton(self.scrollable_frame, text=i, variable=self.conf, value=i, bg="#d5e8d8",
                           command=lambda arg=i: self.setConfig(arg))
            button.pack(anchor='n')
            self.buttons.append(button)
            self.labels.append(w)

    def deleteConf(self):
        with open('ConfigurationsList.bin', 'rb') as f:
            data_loaded = pickle.load(f)

        for config in data_loaded:
            if config.name == self.data.selected_conf_name:
                data_loaded.remove(config)

        with open('ConfigurationsList.bin', 'wb') as f:
            pickle.dump(data_loaded, f)

        self.readConfFromFile()
        self.showConf()
        self.tkraise()


