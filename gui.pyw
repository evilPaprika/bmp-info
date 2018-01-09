from tkinter import *
from bmp import *
from fractions import Fraction
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
        if hasattr(self, 'frame'): self.frame.destroy() # отчищает окно, если чтото уже есть
        self.desired_img_size = (600, 600)
        self.frame = Frame(self.master)
        self.frame.pack(fill=BOTH, expand=1)
        self.master.title("BMP metadata viewer")
        self.current_metadata = get_all_bmp_metadata(self.current_image)
        self.img_width = self.current_metadata["width"]
        self.img_height = self.current_metadata["height"]
        self.current_metadata.update({
            "resize factor x": Fraction(int((self.desired_img_size[0] / self.img_width) * 10) / 10).limit_denominator(),
            "resize factor y": Fraction(int((self.desired_img_size[1] / self.img_height) * 10) / 10).limit_denominator()
        })
        self.showImg(get_raw_bitmap(self.current_image))
        self.showButtons()
        vertical_offset = 0
        label_max_width = 0
        for key, val in self.current_metadata.items():
            self.lbl = Label(self.frame, text=(key.ljust(22) + ":  " + str(val)), font=("Courier New", 12))
            self.lbl.place(x=610, y=vertical_offset)
            self.master.update_idletasks()
            if (label_max_width < self.lbl.winfo_width()): label_max_width = self.lbl.winfo_width()
            vertical_offset += 20
        self.master.geometry('{}x{}'.format(1200, 650))

    def showImg(self, bmp_image):
        self.img = PhotoImage(width=self.img_width,height=self.img_height)
        if self.current_metadata["color depth"] == 24:
            colors = [[bmp_image[i+j] for i in range(2, -1, -1)] for j in range(0, len(bmp_image)-3, 3)]
        elif self.current_metadata["color depth"] == 32:
            colors = [[bmp_image[i+j] for i in range(2, -1, -1)] for j in range(0, len(bmp_image)-4, 4)]
        elif self.current_metadata["color depth"] == 8:
            colors = [[bmp_image[j] for i in range(0, 3)] for j in range(0, len(bmp_image))]
        else:
            colors = [[bmp_image[i + j] for i in range(2, -1, -1)] for j in range(0, len(bmp_image) - 3, 3)]

        row = 0; col = 0
        for color in colors:
            self.img.put('#%02x%02x%02x' % tuple(color),(col,self.img_height - row))

            col += 1
            if col == self.img_width:
               row +=1; col = 0

        self.img = self.resize_img(self.img, self.desired_img_size[0], self.desired_img_size[1])
        label = Label(self.frame, image=self.img)
        label.place(x=0, y=0)


    def showButtons(self):
        self.but1 = Button(self.frame, text="prev", command=self.click_prev)
        self.but1.config(width=10)
        self.but1.place(x=2, y=620)

        self.but2 = Button(self.frame, text="next", command=self.click_next)
        self.but2.config(width=10)
        self.but2.place(x=500, y=620)

    def resize_img(self, img, height, width):
        img_height = img.height()
        img_width = img.width()
        scale_w = Fraction(int((width / img_width)*10)/10).limit_denominator()
        scale_h = Fraction(int((height / img_height)*10)/10).limit_denominator()
        img = img.zoom(scale_w.numerator, scale_h.numerator)
        return img.subsample(scale_w.denominator, scale_h.denominator)

    def click_next(self):
        self.current_image = self.images_list[(self.images_list.index(self.current_image) + 1) % len(self.images_list)]
        self.init_window()

    def click_prev(self):
        self.current_image = self.images_list[(self.images_list.index(self.current_image) - 1) % len(self.images_list)]
        self.init_window()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        images_folder = sys.argv[1]
    else: images_folder = "test-images"
    root = Tk()
    root.geometry("1000x800")
    app = Window(images_folder, root)
    root.mainloop()