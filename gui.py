from tkinter import *
from PIL import Image, ImageTk
from bmp import *


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("BMP metadata viewer")
        self.pack(fill=BOTH, expand=1)
        self.showImg()
        i = 0
        for key, val in get_all_metadata('lena_gray.bmp').items():
            text = Label(self, text=(key + ":  " + str(val)))
            text.place(x=self.img_width + 5, y=i)
            i += 20


    def showImg(self):
        load = Image.open("lena_gray.bmp")
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        self.img_width = render.width()
        self.img_height = render.height()
        img.place(x=0, y=0)

    def showText(self):
        text = Label(self, text="Hey there good lookin!")
        text.pack()

    def client_exit(self):
        exit()


if __name__ == '__main__':
    root = Tk()
    root.geometry("1000x800")
    app = Window(root)
    root.mainloop()