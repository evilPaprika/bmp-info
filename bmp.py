import math

def get_bitmap_file_header_info(filename):
    with open(filename, "rb") as binary_file:
        bitmap = binary_file.read(14)
        if bitmap[:2].decode("ascii") not in ['BM', 'BA', 'CI', 'CP', 'IC', 'PT']:
            raise ValueError("file is not bitmap image file")
        return { "header field" : bitmap[:2].decode("ascii"),
                 "file size bytes" : int.from_bytes(bitmap[2:6], byteorder="little"),
                 "offset": int.from_bytes(bitmap[10:12], byteorder="little"),
                }


def get_bitmap_info_header(file):
    pass

def get_bmp_version(bitmap_file_header):
    pass

def get_width_and_height(bitmap_info_header):
    pass

def convert_size(size_bytes):
    """
     взято со stackoverflow:
     http://stackoverflow.com/a/14822210
    """
    if (size_bytes == 0):
        return '0B'
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes/p, 2)
    return '%s %s' % (s, size_name[i])

if __name__ == '__main__':
    header_info = get_bitmap_file_header_info("test images/Untitled.bmp")
    print(header_info["header field"])
    print(convert_size(header_info["file size bytes"]))
    print(header_info["offset"])
