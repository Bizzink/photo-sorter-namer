from tkinter import *
from tkinter import ttk


class Inter:
    def __init__(self, get_files, copy_files):
        self.root = Tk()
        self.root.title("Photo sorter namer")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.source_path = StringVar()
        self.dest_path = StringVar()
        self.file_count = StringVar()
        self.name_format = StringVar()
        self.name_format.set('%o_%d-%m-%Y_%H-%M-%S')
        self.file_types = StringVar()
        self.file_types.set("png, jpg")

        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky=(N, S, W, E))
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(0, weight=1)

        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=0, column=0, sticky=(W, E))
        controls_frame.columnconfigure(0, weight=1)
        controls_frame.rowconfigure(0, weight=1)

        self.add_entry("Source path: ", 0, self.source_path, controls_frame)
        self.add_entry("File types: ", 1, self.file_types, controls_frame, vcmd=get_files)

        type_frame = ttk.Frame(controls_frame)
        type_frame.grid(column=0, row=2, sticky=(W, E))
        ttk.Button(type_frame, text="Check", command=get_files).grid(column=0, row=0, sticky=(W, E))
        ttk.Label(type_frame, textvariable=self.file_count).grid(column=1, row=0, sticky=(W, E))
        ttk.Label(controls_frame, text="").grid(column=0, row=3)
        self.add_entry("Name format: ", 4, self.name_format, controls_frame)
        self.add_entry("Destination path", 5, self.dest_path, controls_frame)
        ttk.Button(controls_frame, text="Confirm", command=copy_files).grid(column=0, row=6, sticky=(W, S))

        ttk.Separator(main_frame, orient="vertical").grid(column=1, row=0)

        # prefixes
        prefix_main_frame = ttk.Frame(main_frame)
        prefix_main_frame.grid(column=2, row=0, sticky=(N, W, E, S))
        prefix_main_frame.columnconfigure(0, weight=1)
        ttk.Button(prefix_main_frame, text="Add Prefix", command=self.add_range).grid(column=0, row=0, sticky=(W, E, N))
        self.prefix_frame = ttk.Frame(prefix_main_frame)
        self.prefix_frame.grid(column=0, row=1, sticky=(N, W, E, S))
        self.prefix_frame.columnconfigure(0, weight=1)
        self.prefix_frame.columnconfigure(1, weight=1)
        self.prefix_frame.columnconfigure(2, weight=1)
        self.prefix_frame.columnconfigure(3, weight=1)
        self.prefix_frame.columnconfigure(4, weight=1)
        ttk.Label(self.prefix_frame, text="start date             ").grid(column=0, row=0, sticky=(W, E, S))
        ttk.Separator(self.prefix_frame, orient="vertical").grid(column=1, row=0, sticky=(W, E))
        ttk.Label(self.prefix_frame, text="end date             ").grid(column=2, row=0, sticky=(W, E, S))
        ttk.Separator(self.prefix_frame, orient="vertical").grid(column=3, row=0, sticky=(W, E))
        ttk.Label(self.prefix_frame, text="name             ").grid(column=4, row=0, sticky=(W, E, S))

        self.message = StringVar()
        ttk.Label(self.root, textvariable=self.message).grid(row=1, column=0, sticky=(N, W, E))

        self.curr_range = 1
        self.ranges = []

        self.root.update()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        self.root.minsize(w, h)

    def add_entry(self, label, row, variable, controls_frame, vcmd=None):
        """add title /  entry pair"""
        frame = ttk.Frame(controls_frame)
        frame.grid(column=0, row=row, sticky=(W, E, S))
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text=label).grid(column=0, row=0, sticky=W)

        # Add command to run on each update if vcmd is not none
        if vcmd is None:
            entry = ttk.Entry(frame, width=20, textvariable=variable)
        else:
            entry = ttk.Entry(frame, width=20, textvariable=variable, validatecommand=vcmd, validate="focusout")

        entry.grid(column=1, row=0, sticky=(W, E))

    def add_range(self):
        """add new range input"""
        date_range = {"start": StringVar(), "end": StringVar(), "name": StringVar()}

        if self.curr_range == 1:
            date_range["start"].set("1996-09-28")
            date_range["end"].set("25-07-2013")
            date_range["name"].set("Example")

        ttk.Entry(self.prefix_frame, width=10, textvariable=date_range["start"]).grid(column=0, row=self.curr_range, sticky=(W, E))
        ttk.Separator(self.prefix_frame, orient="vertical").grid(column=1, row=self.curr_range, sticky=(W, E))
        ttk.Entry(self.prefix_frame, width=10,  textvariable=date_range["end"]).grid(column=2, row=self.curr_range, sticky=(W, E))
        ttk.Separator(self.prefix_frame, orient="vertical").grid(column=3, row=self.curr_range, sticky=(W, E))
        ttk.Entry(self.prefix_frame, width=10,  textvariable=date_range["name"]).grid(column=4, row=self.curr_range, sticky=(W, E))

        self.ranges.append(date_range)
        self.curr_range += 1


class ErrorMsg:
    def __init__(self, message, message2 = None):
        root = Tk()
        root.title("Error!")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        ttk.Label(root, text=message, anchor="center", pad=20).grid(row=0, column=0, sticky=(W, E))

        if message2 is not None:
            ttk.Label(root, text=message2, anchor="center", pad=20).grid(row=1, column=0, sticky=(W, E))
            ttk.Button(root, text="close", command=root.destroy).grid(row=2, column=0, sticky=(W, E))

        else:
            ttk.Button(root, text="close", command=root.destroy).grid(row=1, column=0, sticky=(W, E))

        root.update()
        w, h = root.winfo_width(), root.winfo_height()
        root.minsize(w, h)
        root.resizable(0, 0)

        root.mainloop()