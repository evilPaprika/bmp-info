

def get_bitmap_file_header(filename):
    with open(filename, "rb") as binary_file:
        print(binary_file.read(14))


def get_bitmap_info_header(file):
    pass

def get_bmp_version(bitmap_file_header):
    pass

def get_width_and_height(bitmap_info_header):
    pass

if __name__ == '__main__':
    get_bitmap_file_header("test images/when-my-code-works-300x200.bmp")
