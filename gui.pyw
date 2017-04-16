from tkinter import *
from PIL import Image, ImageTk
from bmp import *
import sys, glob


class Window(Frame):
    def __init__(self, folder_path, master=None):
        Frame.__init__(self, master)
        self.master = master
        os.chdir(folder_path)
        self.images_list = glob.glob("*.bmp")
        self.current_image = self.images_list[0]
        self.init_window()

    def init_window(self):
        self.frame = Frame(self.master)
        self.frame.pack(fill=BOTH, expand=1)
        self.master.title("BMP metadata viewer")
        self.showImg(self.current_image)
        self.showButtons()
        vertical_offset = 0
        label_max_width = 0
        for key, val in get_all_metadata(self.current_image).items():
            self.lbl = Label(self.frame, text=(key.ljust(22) + ":  " + str(val)), font=("Courier New", 12))
            self.lbl.place(x=self.img_width + 10, y=vertical_offset)
            self.master.update_idletasks()
            if (label_max_width < self.lbl.winfo_width()): label_max_width = self.lbl.winfo_width()
            vertical_offset += 20
        self.master.geometry('{}x{}'.format(self.img_width + label_max_width + 10, max(vertical_offset - 30, self.img_height)+50))

    def showImg(self, image):
        load = Image.open(image)
        render = ImageTk.PhotoImage(load)
        img = Label(self.frame, image=render)
        img.image = render
        self.img_width = render.width()
        self.img_height = render.height()
        img.place(x=0, y=0)

    def showButtons(self):
        self.but1 = Button(self.frame, text="prev", command=self.click_prev)
        self.but1.config(width=10)
        self.but1.place(x=2, y=self.img_height+10)

        self.but2 = Button(self.frame, text="next", command=self.click_next)
        self.but2.config(width=10)
        self.but2.place(x=self.img_width-78, y=self.img_height+10)

    def click_next(self):
        self.current_image = self.images_list[(self.images_list.index(self.current_image) - 1) % len(self.images_list)]
        self.frame.destroy()
        self.init_window()

    def click_prev(self):
        self.current_image = self.images_list[(self.images_list.index(self.current_image) + 1) % len(self.images_list)]
        self.frame.destroy()
        self.init_window()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        images_folder = sys.argv[1]
    else: images_folder = "test-images"
    #else: print("usage: bmp.exe <image-name.bmp>")
    root = Tk()
    root.geometry("1000x800")
    app = Window(images_folder, root)
    root.mainloop()