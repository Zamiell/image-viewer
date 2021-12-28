import getpass
import glob
import os
import tkinter
from PIL import Image, ImageTk

# Constants
USERNAME = getpass.getuser()
SCREENSHOTS_DIRECTORY = (
    "C:\\Users\\{}\\AppData\\Roaming\\StardewValley\\Screenshots".format(USERNAME)
)
WINDOW_X = 1913
WINDOW_Y = 0
WINDOW_WIDTH = 958
WINDOW_HEIGHT = 1048
CHECK_INTERVAL_MILLISECONDS = 100

# Variables
window = tkinter.Tk()
label = tkinter.Label(window)
image = None  # To prevent garbage collection


def main():
    window.title("Image Viewer")
    window.geometry(
        "{}x{}+{}+{}".format(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_X, WINDOW_Y)
    )
    label.bind("<Configure>", resize_image)
    label.pack(fill=tkinter.BOTH, expand=tkinter.YES)

    # Check for new images in an infinite loop
    read_file_loop()

    window.mainloop()


def resize_image(event):
    read_file_loop(False)


def read_file_loop(loop=True):
    global image
    global current_file_name

    window_width = window.winfo_width()
    window_height = window.winfo_height()

    try:
        png_files = glob.glob("{}\\*.png".format(SCREENSHOTS_DIRECTORY))
        if len(png_files) == 0:
            return

        newest_png_path = max(png_files, key=os.path.getctime)
        newest_png = Image.open(newest_png_path)

    except Exception as e:
        printf(e)
        return

    # From: https://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio
    ratio = min(window_width / newest_png.width, window_height / newest_png.height)
    new_width = max(int(newest_png.width * ratio), 1)
    new_height = max(int(newest_png.height * ratio), 1)

    resized_png = newest_png.resize((new_width, new_height))
    image = ImageTk.PhotoImage(resized_png)
    label.configure(image=image)

    if loop:
        window.after(CHECK_INTERVAL_MILLISECONDS, read_file_loop)


def printf(*args):
    print(*args, flush=True)


if __name__ == "__main__":
    main()
