from bmp import *
import unittest

class TestMetadataExtractor(unittest.TestCase):
    def test_headers_extraction_length(self):
        self.assertEqual(len(get_headers("test-images/when-my-code-works-300x200.bmp")), 138)
        self.assertEqual(len(get_headers("test-images/debugging.bmp")), 54)
        self.assertEqual(len(get_headers("test-images/Untitled.bmp")), 54)
        self.assertEqual(len(get_headers("test-images/LAND.BMP")), 1078)

    def test_bitmap_version(self):
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/when-my-code-works-300x200.bmp"))['BMP version'], 'Windows V5')
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/debugging.bmp"))['BMP version'], 'Windows V3')
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/Untitled.bmp"))['BMP version'], 'Windows V3')
        self.assertEqual(get_bitmap_info_dict(get_headers("test-images/LAND.BMP"))['BMP version'], 'Windows V3')


if __name__ == '__main__':
    unittest.main()