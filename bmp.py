import math
import os
import ntpath
import time

def get_headers(filename):
    with open(filename, "rb") as binary_file:
        bitmap_headers = binary_file.read(14)
        if bitmap_headers[:2].decode("ascii") not in ['BM', 'BA', 'CI', 'CP', 'IC', 'PT']:
            raise ValueError("file is not bitmap image file")
        offset = int.from_bytes(bitmap_headers[10:12], byteorder="little")
        bitmap_headers += binary_file.read(offset - 14)
    return bitmap_headers


def get_all_metadata(filename):
    bitmap_headers = get_headers(filename)
    result = {
        "path" : os.path.dirname(os.path.realpath(filename)),
        "filename" : ntpath.basename(filename),
        "created" : time.ctime(os.path.getctime(filename)),
        "modified": time.ctime(os.path.getmtime(filename))

    }
    result.update(get_bitmap_file_header_dict(bitmap_headers))
    result.update(get_bitmap_info_dict(bitmap_headers))
    return result

def get_bitmap_file_header_dict(bitmap_headers):
    """
     Обрабатывает хедер файла, и возвращает словарь данных
    """
    return {
            "header field" : bitmap_headers[:2].decode("ascii"),
            "file size" : convert_size(int.from_bytes(bitmap_headers[2:6], byteorder="little")),
            "offset": int.from_bytes(bitmap_headers[10:12], byteorder="little"),
           }

def get_bitmap_info_dict(bitmap_headers):
    """
     Находит размер заголовочной информации, вызывает соответствующий
     обработчик, и возвращает словарь данных
    """
    bitmap_info_size = int.from_bytes(bitmap_headers[14:16], byteorder="little")
    result_dict = { "bitmap info size": bitmap_info_size }
    if bitmap_info_size == 40:
        result_dict.update({"BMP version": "Windows V3"})
        result_dict.update(get_bitmap_V3_header_dict(bitmap_headers))
    elif bitmap_info_size == 108:
        result_dict.update({"BMP version": "Windows V4"})
        result_dict.update(get_bitmap_V4_header_dict(bitmap_headers))
    elif bitmap_info_size == 124:
        result_dict.update({"BMP version": "Windows V5"})
        result_dict.update(get_bitmap_V5_header_dict(bitmap_headers))
    return result_dict

def get_bitmap_V3_header_dict(bitmap_info):
    return {
        "width" : int.from_bytes(bitmap_info[18:22], byteorder="little"),
        "height" : int.from_bytes(bitmap_info[22:26], byteorder="little"),
        "number of panels" : int.from_bytes(bitmap_info[26:28], byteorder="little"),
        "color depth": int.from_bytes(bitmap_info[28:30], byteorder="little"),
        "compression method": int.from_bytes(bitmap_info[30:34], byteorder="little") or "none",
        "image size": convert_size(int.from_bytes(bitmap_info[34:38], byteorder="little")),
        "horizontal resolution": int.from_bytes(bitmap_info[38:42], byteorder="little", signed=True),
        "vertical resolution": int.from_bytes(bitmap_info[42:46], byteorder="little", signed=True),
        "num colors": int.from_bytes(bitmap_info[46:50], byteorder="little") or "unindexed",
        "num important colors": int.from_bytes(bitmap_info[50:54], byteorder="little")
    }

def get_bitmap_V4_header_dict(bitmap_info):
    result_dict = get_bitmap_V3_header_dict(bitmap_info)
    result_dict.update({
        "red mask": "{0:#010x}".format((int.from_bytes(bitmap_info[54:58], byteorder="little"))),
        "green mask": "{0:#010x}".format(int.from_bytes(bitmap_info[58:62], byteorder="little")),
        "blue mask": "{0:#010x}".format(int.from_bytes(bitmap_info[62:66], byteorder="little")),
        "alpha mask": "{0:#010x}".format(int.from_bytes(bitmap_info[66:70], byteorder="little")),
        "color space type": bitmap_info[70:74].decode('ascii')[::-1]
    })
    if (result_dict["color space type"] == 0):
        result_dict.update({
            "end points": int.from_bytes(bitmap_info[74:110], byteorder="little"),
            "gamma red": int.from_bytes(bitmap_info[110:114], byteorder="little"),
            "gamma green": int.from_bytes(bitmap_info[114:118], byteorder="little"),
            "gamma blue": int.from_bytes(bitmap_info[118:122], byteorder="little"),
        })
    return result_dict

def get_bitmap_V5_header_dict(bitmap_info):
    result_dict = get_bitmap_V4_header_dict(bitmap_info)
    result_dict.update({
        "intent": int.from_bytes(bitmap_info[122:126], byteorder="little"),
        "profile data": int.from_bytes(bitmap_info[126:130], byteorder="little"),
        "profile size": int.from_bytes(bitmap_info[130:134], byteorder="little"),
    })
    return result_dict


def convert_size(size_bytes):
    """
     Взято со stackoverflow:
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
    filename = "test-images/when-my-code-works-300x200.bmp"
    bitmap_headers = get_headers(filename)
    print(get_all_metadata(filename))
    print(bitmap_headers)
