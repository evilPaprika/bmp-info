from tkinter import *
from PIL import Image, ImageTk
from bmp import *
import sys


class Window(Frame):
    def __init__(self, image_path, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.image_path = image_path
        self.init_window()

    def init_window(self):
        self.master.title("BMP metadata viewer")
        self.pack(fill=BOTH, expand=1)
        self.showImg()
        i = 0
        for key, val in get_all_metadata(self.image_path).items():
            text = Label(self, text=(key.ljust(25) + ":   " + str(val)), font=("Courier New", 12))
            text.place(x=self.img_width + 10, y=i)
            i += 20
        self.master.geometry('{}x{}'.format(self.img_width + 700, max(i, self.img_height)+20))

    def showImg(self):
        load = Image.open(self.image_path)
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        self.img_width = render.width()
        self.img_height = render.height()
        img.place(x=0, y=0)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    #else: image_path = "test-images\when-my-code-works-300x200.bmp"
    else: print("usage: bmp.exe <image-name.bmp>")
    root = Tk()
    root.geometry("1000x800")
    app = Window(image_path, root)
    root.mainloop()