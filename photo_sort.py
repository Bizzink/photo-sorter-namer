import inter
import os
import shutil
import datetime

imgs = []
date_ranges = {}
prev = None


def get_imgs():
    """find all files in any subdirectory, if its filetype is in types, add it to imgs, set img_count to amount of files found"""
    global imgs
    imgs = []

    # convert types from string to list of file extensions
    types = ui.img_types.get()
    types = types.split(", ")

    # add . at start of extension
    for i in range(len(types)):
        if not types[i][0] == ".":
            types[i] = "." + types[i]

    for root, dirs, files in os.walk(ui.source_path.get()):
        for file in files:
            # separate file name and extension
            name, ext = os.path.splitext(f"{root}\\{file}")

            # if file is correct type
            if str(ext) in types:
                # get earlier of creation time (ctime), modification time (mtime)
                date = datetime.datetime.fromtimestamp(min(os.path.getmtime(f"{root}\\{file}"), os.path.getctime(f"{root}\\{file}")))

                imgs.append({"path": f"{root}\\{file}", "name": file, "ext": ext, "date": date})

    ui.img_count.set(f" {len(imgs)} files found.")


def str_to_datetime(string):
    """convert date string (from date ranges entry) to datetime format"""
    global prev

    # preset vals
    if string == "today":
        return datetime.datetime.today()

    if string == "prev":
        return prev

    # get year month, day depending on order they were entered
    date = string.split("-")
    if len(date[0]) == 4:
        year, month, day = date

    elif len(date[2]) == 4:
        day, month, year = date

    else:
        raise ValueError("Invalid date format")

    try:
        date = datetime.datetime(int(year), int(month), int(day))
    except:
        raise ValueError("Invalid date format")

    return date


def add_range(date_range):
    """add a date range to ranges"""
    global prev

    name = date_range["name"].get()
    start = date_range["start"].get()
    end = date_range["end"].get()

    try:
        start = str_to_datetime(start)
    except ValueError:
        inter.ErrorMsg(f"Invalid start date format in range '{name}'! ({start})", message2=f"Format should be 'yyyy-mm-dd' or 'dd-mm-yyyy'")
        return False

    try:
        end = str_to_datetime(end)
    except ValueError:
        inter.ErrorMsg(f"Invalid start date format in range '{name}'! ({end})", message2=f"Format should be 'yyyy-mm-dd' or 'dd-mm-yyyy'")
        return False

    prev = end
    date_ranges[name] = {"start": start, "end": end}
    return True


def in_range(date):
    """check if a date falls within a date range, if it does, return name of range"""
    for key in date_ranges.keys():
        if date_ranges[key]["start"] <= date <= date_ranges[key]["end"]:
            return str(key)

    return ""


def copy_imgs():
    """copys all files gotten from get_imgs() to dest_path, renames them based on date format and range prefixes"""
    for date_range in ui.ranges:
        if not add_range(date_range):
            return

    if not os.path.exists(ui.dest_path.get()):
        os.mkdir(ui.dest_path.get())

    dest = ui.dest_path.get()

    not_copied = 0

    for img in imgs:
        try:
            shutil.copy(img["path"], dest)
        except shutil.SameFileError:
            not_copied += 1
            continue

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
                    # add version number if duped name
                    os.rename(f"{dest}\\{name}", f"{dest}\\{new_name}_{dupe}{ext}")
                else:
                    os.rename(f"{dest}\\{name}", f"{dest}\\{new_name}{ext}")
                success = True

            except FileExistsError:
                success = False
                dupe += 1

        if dupe != 0:
            rename = f"{prefix}{date}_{dupe}{ext}"
            print(f"{dest}\\{name}".ljust(60, " ") + f"\t-->\t{dest}\\{prefix}{date}_{dupe}{ext}")
        else:
            rename = f"{prefix}{date}{ext}"
            print(f"{dest}\\{name}".ljust(60, " ") + f"\t-->\t{dest}\\{prefix}{date}{ext}")

        ui.message.set(f"{name} --> {rename}")
        ui.root.update()

    if not_copied > 0:
        ui.message.set(f"{not_copied} files not copied (already exist in destination folder)")
        ui.root.update()


if __name__ == "__main__":
    ui = inter.Inter(get_imgs, copy_imgs)
    ui.root.mainloop()
