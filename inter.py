from tkinter import *
from tkinter import ttk


class Inter:
    def __init__(self, toggle_png, toggle_jpg, copy_imgs):
        self.root = Tk()
        self.root.title("Photo sorter namer")
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky=(N, W, E, S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        self.source_path = StringVar()
        self.dest_path = StringVar()
        self.img_count = StringVar()
        self.img_count.set("Image types: 0 found.")
        self.date_format = StringVar()
        self.date_format.set('%d-%m-%Y_%H-%M-%S')
        self.png = BooleanVar()
        self.png.set(False)
        self.jpg = BooleanVar()
        self.jpg.set(False)

        self.add_entry("Source path: ", 0, self.source_path, main_frame)
        self.add_entry("Date format: ", 3, self.date_format, main_frame)
        ttk.Separator(main_frame, orient="horizontal").grid(column=0, row=4)
        self.add_entry("Destination path", 5, self.dest_path, main_frame)
        ttk.Button(main_frame, text="Confirm", command=copy_imgs).grid(column=0, row=6, sticky=(W, E, S))
        ttk.Separator(self.root, orient="vertical").grid(column=1, row=0)

        # Img Types
        types_frame = ttk.Frame(main_frame)
        types_frame.grid(column=0, row=1, sticky=(W, E, N))
        ttk.Label(types_frame, textvariable=self.img_count).grid(column=0, row=0, sticky=W)
        ttk.Checkbutton(types_frame, text="PNG", variable=self.png, command=toggle_png).grid(column=0, row=1, sticky=W)
        ttk.Checkbutton(types_frame, text="JPG", variable=self.jpg, command=toggle_jpg).grid(column=1, row=1, sticky=W)

        # prefixes
        prefix_main_frame = ttk.Frame(self.root)
        prefix_main_frame.grid(column=2, row=0, sticky=(N, W, E, S))
        prefix_main_frame.columnconfigure(0, weight=1)
        ttk.Button(prefix_main_frame, text="Add Prefix", command=self.add_range).grid(column=0, row=0, sticky=(W, E, N))
        self.prefix_frame = ttk.Frame(prefix_main_frame)
        self.prefix_frame.grid(column=0, row=1, sticky=(N, W, E, S))
        self.prefix_frame.columnconfigure(0, weight=1)
        self.prefix_frame.columnconfigure(1, weight=1)
        self.prefix_frame.columnconfigure(2, weight=1)
        ttk.Label(self.prefix_frame, text="start date").grid(column=0, row=0, sticky=(W, E, S))
        ttk.Separator(self.prefix_frame, orient="vertical").grid(column=1, row=0, sticky=(W, E))
        ttk.Label(self.prefix_frame, text="end date").grid(column=2, row=0, sticky=(W, E, S))
        ttk.Separator(self.prefix_frame, orient="vertical").grid(column=3, row=0, sticky=(W, E))
        ttk.Label(self.prefix_frame, text="name").grid(column=4, row=0, sticky=(W, E, S))

        self.curr_range = 1
        self.ranges = []

    def add_entry(self, label, row, variable, main_frame):
        frame = ttk.Frame(main_frame)
        frame.grid(column=0, row=row, sticky=(W, E, S))
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text=label).grid(column=0, row=0, sticky=W)

        entry = ttk.Entry(frame, width=30, textvariable=variable)
        entry.grid(column=1, row=0, sticky=(W, E))

    def add_range(self):
        date_range = {"start": StringVar(), "end": StringVar(), "name": StringVar()}

        if self.curr_range == 1:
            date_range["start"].set("1996-09-28")
            date_range["end"].set("1997-02-13")
            date_range["name"].set("Example")

        ttk.Entry(self.prefix_frame, width=10, textvariable=date_range["start"]).grid(column=0, row=self.curr_range, sticky=(W, E))
        ttk.Separator(self.prefix_frame, orient="vertical").grid(column=1, row=self.curr_range, sticky=(W, E))
        ttk.Entry(self.prefix_frame, width=10,  textvariable=date_range["end"]).grid(column=2, row=self.curr_range, sticky=(W, E))
        ttk.Separator(self.prefix_frame, orient="vertical").grid(column=3, row=self.curr_range, sticky=(W, E))
        ttk.Entry(self.prefix_frame, width=10,  textvariable=date_range["name"]).grid(column=4, row=self.curr_range, sticky=(W, E))

        self.ranges.append(date_range)
        self.curr_range += 1
