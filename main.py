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


def main():
    window = tkinter.Tk()
    ImageViewer(window)
    window.title("Image Viewer")
    window.geometry(
        "{}x{}+{}+{}".format(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_X, WINDOW_Y)
    )

    window.mainloop()


class ImageViewer(tkinter.Frame):
    def __init__(self, parent, *args, **kwargs):
        tkinter.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.label = tkinter.Label(self.parent)
        self.image = None

        self.label.bind("<Configure>", self.resize_image)
        self.label.pack(fill=tkinter.BOTH, expand=tkinter.YES)

        self.parent.after(CHECK_INTERVAL_MILLISECONDS, self.read_file_loop)

    def resize_image(self, event):
        self.read_file_loop(False)

    def read_file_loop(self, loop=True):
        if loop:
            self.parent.after(CHECK_INTERVAL_MILLISECONDS, self.read_file_loop)

        try:
            window_width = self.parent.winfo_width()
            window_height = self.parent.winfo_height()

            png_files = glob.glob("{}\\*.png".format(SCREENSHOTS_DIRECTORY))
            if len(png_files) == 0:
                return

            newest_png_path = max(png_files, key=os.path.getctime)

            # Try to rename the file to itself
            # In the case where the file is currently being written to, this will fail and will prevent corrupting the file
            # From: https://stackoverflow.com/a/37256114/1062714
            os.rename(newest_png_path, newest_png_path)

            newest_png = Image.open(newest_png_path)

            # From: https://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio
            ratio = min(
                window_width / newest_png.width, window_height / newest_png.height
            )
            new_width = max(int(newest_png.width * ratio), 1)
            new_height = max(int(newest_png.height * ratio), 1)

            # Resizing can fail if the file was only partially read
            resized_png = newest_png.resize((new_width, new_height))
            self.image = ImageTk.PhotoImage(resized_png)
            self.label.configure(image=self.image)
            # printf("Set new image: {}".format(image))

        # Exceptions can occur if the screenshot is read before it is finished being written to
        # If this is the case, do nothing and wait for the next interval
        except Exception as e:
            return


def printf(*args):
    print(*args, flush=True)


if __name__ == "__main__":
    main()
