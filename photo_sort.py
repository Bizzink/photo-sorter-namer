import inter
import os
import shutil
import datetime

imgs = []
types = []
date_ranges = {}
prev = None


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
    global types, imgs
    imgs = []

    for root, dirs, files in os.walk(ui.source_path.get()):
        for file in files:
            name, ext = os.path.splitext(f"{root}\\{file}")

            if str(ext) in types:
                # earlier of creation, modification time
                date = datetime.datetime.fromtimestamp(min(os.path.getmtime(f"{root}\\{file}"), os.path.getctime(f"{root}\\{file}")))

                imgs.append({"path": f"{root}\\{file}", "name": file, "ext": ext,
                             "date": date})

    ui.img_count.set(f"Image types: {len(imgs)} found.")


def str_to_datetime(string):
    global prev
    string = string.get()

    if string == "today":
        return datetime.datetime.today()

    if string == "prev":
        return prev

    year, month, day = string.split("-")
    date = datetime.datetime(int(year), int(month), int(day))
    return date


def add_range(date_range):
    global prev
    start = str_to_datetime(date_range["start"])
    end = str_to_datetime(date_range["end"])
    name = date_range["name"].get()

    prev = end

    date_ranges[name] = {"start": start, "end": end}


def in_range(date):
    for key in date_ranges.keys():
        if date_ranges[key]["start"] <= date <= date_ranges[key]["end"]:
            return str(key)

    return ""


def copy_imgs():
    if not os.path.exists(ui.dest_path.get()):
        os.mkdir(ui.dest_path.get())

    for date_range in ui.ranges:
        add_range(date_range)

    for img in imgs:
        dest = ui.dest_path.get()

        shutil.copy(img["path"], dest)

        name = img["name"]
        ext = img["ext"]
        date = img["date"].strftime(ui.date_format.get())
        prefix = in_range(img["date"])

        dupe = 0
        success = False

        new_name = f"{prefix}_{date}"

        # Duplicate creation date handling
        while not success:
            try:
                if dupe != 0:
                    os.rename(f"{dest}\\{name}", f"{dest}\\{new_name}_{dupe}{ext}")
                else:
                    os.rename(f"{dest}\\{name}", f"{dest}\\{new_name}{ext}")
                success = True

            except FileExistsError:
                success = False
                dupe += 1

        print(f"{dest}\\{name}".ljust(60, " ") + f"\t-->\t{dest}\\{date}{ext}")


if __name__ == "__main__":
    ui = inter.Inter(toggle_png, toggle_jpg, copy_imgs)
    ui.root.mainloop()
