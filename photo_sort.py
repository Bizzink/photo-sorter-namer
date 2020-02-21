from tkinter import *
from tkinter import ttk
import os
import shutil
from datetime import datetime

imgs = []
types = []


def toggle_png():
    if ".png" in types:
        types.remove(".png")
    else:
        types.append(".png")

    get_imgs()


def toggle_jpg():
    if ".jpg" in types:
        types.remove(".jpg")
    else:
        types.append(".jpg")

    get_imgs()


def get_imgs():
    global source_path, types, imgs

    imgs = []

    for root, dirs, files in os.walk(source_path.get()):
        for file in files:
            name, ext = os.path.splitext(f"{root}\\{file}")

            if str(ext) in types:
                date = os.path.getctime(f"{root}\\{file}")
                date = datetime.utcfromtimestamp(date).strftime(date_format.get())

                imgs.append({"path": f"{root}\\{file}", "name": file, "ext": ext,
                             "date": date})

    update_img_count(len(imgs))


def make_dest_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)


def copy_imgs():
    make_dest_folder(dest_path.get())

    print(dest_path.get())

    for img in imgs:
        dest = dest_path.get()

        shutil.copy(img["path"], dest)

        name = img["name"]
        ext = img["ext"]
        date = img["date"]

        dupe = 0
        success = False

        # Duplicate creation date handling
        while not success:
            try:
                if dupe != 0:
                    os.rename(f"{dest}\\{name}", f"{dest}\\{date}_{dupe}{ext}")
                else:
                    os.rename(f"{dest}\\{name}", f"{dest}\\{date}{ext}")
                success = True

            except FileExistsError:
                success = False
                dupe += 1

        print(f"{dest}\\{name}".ljust(60, " ") + f"\t-->\t{dest}\\{date}{ext}")


def update_img_count(val):
    if val == 1:
        img_count.set(f"Found {val} image.")
    else:
        img_count.set(f"Found {val} images.")


root = Tk()
root.title("Photo sorter namer")

source_path = StringVar()
dest_path = StringVar()
img_count = StringVar()
date_format = StringVar()
date_format.set('%Y-%m-%d_%H-%M-%S')

# Source path
source_frame = ttk.Frame(root)
source_frame.grid(column=0, row=0, sticky=(W, E, N))
ttk.Label(source_frame, text="Source path:").grid(column=0, row=0, sticky=(W, E))
source_entry = ttk.Entry(source_frame, width=50, textvariable=source_path, foreground="white")
source_entry.grid(column=1, row=0, sticky=(W, E))

# Img Types
types_frame = ttk.Frame(root)
types_frame.grid(column=0, row=1, sticky=(W, E))
ttk.Label(types_frame, text="Image types:").grid(column=0, row=0, sticky=W)
type_png = ttk.Checkbutton(types_frame, text="PNG", command=toggle_png).grid(column=0, row=1, sticky=W)
type_jpg = ttk.Checkbutton(types_frame, text="JPG", command=toggle_jpg).grid(column=1, row=1, sticky=W)

ttk.Label(root, textvariable=img_count).grid(column=0, row=2, sticky=(W, E))

# Destination path
dest_frame = ttk.Frame(root)
dest_frame.grid(column=0, row=3, sticky=(W, E, S))
ttk.Label(dest_frame, text="Destination path:").grid(column=0, row=0, sticky=(W, E))
dest_entry = ttk.Entry(dest_frame, width=50, textvariable=dest_path, foreground="white")
dest_entry.grid(column=1, row=0, sticky=(W, E))

# Date format
date_frame = ttk.Frame(root)
date_frame.grid(column=0, row=4, sticky=(W, E, S))
ttk.Label(date_frame, text="Date format:").grid(column=0, row=0, sticky=(W, E))
date_entry = ttk.Entry(date_frame, width=50, textvariable=date_format, foreground="white")
date_entry.grid(column=1, row=0, sticky=(W, E))

# confirm
ttk.Button(root, text="Confirm", command=copy_imgs).grid(column=0, row=5, sticky=(S))

if __name__ == "__main__":
    root.mainloop()
