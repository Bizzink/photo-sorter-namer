import inter
import os
import shutil
import datetime

files = []
date_ranges = {}
prev = None


def get_files():
    """find all files in any subdirectory, if its filetype is in types, add it to files, set file_count to amount of files found"""
    global files
    files = []

    # convert types from string to list of file extensions
    types = ui.file_types.get()
    types = types.split(", ")

    print(ui.source_path.get())

    # add . at start of extension
    for i in range(len(types)):
        if not types[i][0] == ".":
            types[i] = "." + types[i]

    for root, dirs, file_names in os.walk(ui.source_path.get()):
        for file in file_names:
            # separate file name and extension
            name, ext = os.path.splitext(file)

            print(root, file)

            # if file is correct type
            if str(ext) in types:
                # get earlier of creation time (ctime), modification time (mtime)
                date = datetime.datetime.fromtimestamp(min(os.path.getmtime(f"{root}\\{file}"), os.path.getctime(f"{root}\\{file}")))

                files.append({"path": f"{root}\\{file}", "name": name, "ext": ext, "date": date})

    ui.file_count.set(f" {len(files)} files found.")


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


def format_name(file):
    """create a filename based on entered name format"""
    name_format = ui.name_format.get()
    new_name = ""

    i = 0
    while i < len(name_format):
        # check for format codes
        if name_format[i] == "%":
            val = name_format[i + 1]

            # %o : original file name
            if val == "o":
                new_name += file["name"]

            # %r : range name
            elif val == "r":
                new_name += in_range(file["date"])

            # %-* for 2 char codes
            elif val == "-":
                new_name += file["date"].strftime(f"%-{name_format[i + 2]}")
                i += 1

            # all other format codes
            else:
                new_name += file["date"].strftime(f"%{val}")

            i += 2

        # include non format chars as normal chars
        else:
            new_name += name_format[i]
            i += 1

    return new_name


def copy_files():
    """copys all files gotten from get_files() to dest_path, renames them based on date format and range prefixes"""
    for date_range in ui.ranges:
        if not add_range(date_range):
            return

    if not os.path.exists(ui.dest_path.get()):
        os.mkdir(ui.dest_path.get())

    dest = ui.dest_path.get()

    not_copied = 0

    for file in files:
        try:
            shutil.copy(file["path"], dest)
        except shutil.SameFileError:
            not_copied += 1
            continue

        except FileNotFoundError:
            continue

        name = file["name"]
        new_name = format_name(file)
        ext = file["ext"]

        dupe = 0
        success = False

        # Duplicate creation date handling
        while not success:
            try:
                if dupe != 0:
                    # add version number if duped name
                    os.rename(f"{dest}\\{name}{ext}", f"{dest}\\{new_name}_{dupe}{ext}")
                else:
                    os.rename(f"{dest}\\{name}{ext}", f"{dest}\\{new_name}{ext}")
                success = True

            except FileExistsError:
                success = False
                dupe += 1

        if dupe != 0:
            rename = f"{new_name}_{dupe}{ext}"
            print(f"{dest}\\{name}{ext}".ljust(60, " ") + f"\t-->\t{dest}\\{new_name}_{dupe}{ext}")
        else:
            rename = f"{new_name}{ext}"
            print(f"{dest}\\{name}{ext}".ljust(60, " ") + f"\t-->\t{dest}\\{new_name}{ext}")

        ui.message.set(f"{name}{ext} --> {rename}")
        ui.root.update()

    if not_copied > 0:
        ui.message.set(f"{not_copied} files not copied (already exist in destination folder)")
        ui.root.update()


if __name__ == "__main__":
    ui = inter.Inter(get_files, copy_files)
    ui.root.mainloop()
