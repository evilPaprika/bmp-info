from bmp import *
import unittest

class TestMetadataExtractor(unittest.TestCase):
    def test_headers_extraction_length(self):
        self.assertEqual(len(get_headers("test-images/RAY.BMP")), 54)
        self.assertEqual(len(get_headers("test-images/1lena_gray.bmp")), 1078)
        self.assertEqual(len(get_headers("test-images/2test-image.bmp")), 54)

    def test_bitmap_version(self):
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/RAY.BMP"))['BMP version'], 'Windows V3')
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/Untitled.bmp"))['BMP version'], 'Windows V3')
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/2test-image.bmp"))['BMP version'], 'Windows V3')
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/when-my-code-works-300x200.bmp"))['BMP version'], 'Windows V5')

    def test_bitmap_file_size(self):
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/RAY.BMP"))['file size'], '1.37 MB')
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/Untitled.bmp"))['file size'], '1.03 MB')
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/2test-image.bmp"))['file size'], '732.47 KB')

    def test_bitmap_width_and_height(self):
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/RAY.BMP"))['width'], 800)
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/Untitled.bmp"))['width'], 524)
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/2test-image.bmp"))['width'], 500)
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/RAY.BMP"))['height'], 600)
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/Untitled.bmp"))['height'], 687)
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/2test-image.bmp"))['height'], 500)

    def test_bitmap_color_depth(self):
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/RAY.BMP"))['color depth'], 24)
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/1lena_gray.bmp"))['color depth'], 8)
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/2test-image.bmp"))['color depth'], 24)
        self.assertEqual(get_all_bmp_metadata("test-images/when-my-code-works-300x200.bmp")['color depth'], 32)

    def test_bitmap_number_of_panels(self):
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/RAY.BMP"))['number of panels'], 1)
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/1lena_gray.bmp"))['number of panels'], 1)
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/2test-image.bmp"))['number of panels'], 1)

    def test_bitmap_num_colors(self):
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/RAY.BMP"))['num colors'], "unindexed")
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/1lena_gray.bmp"))['num colors'], "unindexed")
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/2test-image.bmp"))['num colors'], "unindexed")

    def test_bitmap_created_time(self):
        self.assertEqual(get_all_bmp_metadata("test-images/RAY.BMP")['created'], 'Sun Apr 16 14:40:13 2017')
        self.assertEqual(get_all_bmp_metadata("test-images/1lena_gray.bmp")['created'], 'Fri Apr 14 15:04:15 2017')
        self.assertEqual(get_all_bmp_metadata("test-images/2test-image.bmp")['created'], 'Sat May 27 09:11:07 2017')

    def test_bitmap_header_field(self):
        self.assertEqual(get_all_bmp_metadata("test-images/RAY.BMP")['header field'], 'BM')
        self.assertEqual(get_all_bmp_metadata("test-images/1lena_gray.bmp")['header field'], 'BM')
        self.assertEqual(get_all_bmp_metadata("test-images/2test-image.bmp")['header field'], 'BM')

    def test_bitmap_bitmap_info_size(self):
        self.assertEqual(get_all_bmp_metadata("test-images/RAY.BMP")['bitmap info size'], 40)
        self.assertEqual(get_all_bmp_metadata("test-images/1lena_gray.bmp")['bitmap info size'], 40)
        self.assertEqual(get_all_bmp_metadata("test-images/2test-image.bmp")['bitmap info size'], 40)
        self.assertEqual(get_all_bmp_metadata("test-images/when-my-code-works-300x200.bmp")['bitmap info size'], 124)

    def test_bitmap_V5(self):
        self.assertEqual(get_all_bmp_metadata("test-images/when-my-code-works-300x200.bmp")['intent'], 4)
        self.assertEqual(get_all_bmp_metadata("test-images/when-my-code-works-300x200.bmp")['profile data'], 0)
        self.assertEqual(get_all_bmp_metadata("test-images/when-my-code-works-300x200.bmp")['profile size'], 0)


if __name__ == '__main__':
    unittest.main()