import unittest
import os
import sys
import json
import hashlib
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
import convert_to_palette as ctp


def md5(file_name):
    hash_md5 = hashlib.md5()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


class ConvertTest(unittest.TestCase):
    def test_get_symbol_img(self):
        img = ctp.get_symbol_img(' ', 'tests/fonts/font1.ttf')
        self.assertTupleEqual(img.size, (8, 16))
        self.assertListEqual(list(img.getdata()), [0 for _ in range(128)])

    def test_get_codes(self):
        img = ctp.get_symbol_img(' ', 'tests/fonts/font1.ttf')
        codes = ctp.get_codes(img)
        self.assertListEqual([0, 0, 0, 0], codes)

    def test_convert_to_palette(self):
        palette = ctp.convert_to_palette('tests/fonts/font1.ttf')
        self.assertEqual(95, len(palette))
        for s in palette:
            self.assertEqual(len(palette[s]), 4)

    def test_save_palette(self):
        ctp.save_palette('tests/fonts/font1.ttf', 'tests/palettes')
        with open('tests/palettes/font1.plt', 'r') as f:
            palette = json.load(f)
        self.assertEqual(95, len(palette))
        for s in palette:
            self.assertEqual(len(palette[s]), 4)
        os.remove('tests/palettes/font1.plt')

    def test_create_palettes_dir_dir(self):
        ctp.create_palettes('tests/fonts', 'tests/palettes')
        self.assertEqual(md5('tests/palettes/font1.plt'),
                         '1492675b65b49cb575533952dadeb5a2')
        self.assertEqual(md5('tests/palettes/font2.plt'),
                         '64b9346d5e5ee9bd604ad655edf4a887')
        os.remove('tests/palettes/font1.plt')
        os.remove('tests/palettes/font2.plt')

    def test_create_palettes_dir_none(self):
        ctp.create_palettes('tests/fonts', None)
        self.assertEqual(md5('tests/fonts/font1.plt'),
                         '1492675b65b49cb575533952dadeb5a2')
        self.assertEqual(md5('tests/fonts/font2.plt'),
                         '64b9346d5e5ee9bd604ad655edf4a887')
        os.remove('tests/fonts/font1.plt')
        os.remove('tests/fonts/font2.plt')

    def test_create_palettes_name_none(self):
        ctp.create_palettes('tests/fonts/font1.ttf', None)
        self.assertEqual(md5('tests/fonts/font1.plt'),
                         '1492675b65b49cb575533952dadeb5a2')
        os.remove('tests/fonts/font1.plt')

    def test_create_palettes_name_dir(self):
        ctp.create_palettes('tests/fonts/font1.ttf', 'tests/palettes')
        self.assertEqual(md5('tests/palettes/font1.plt'),
                         '1492675b65b49cb575533952dadeb5a2')
        os.remove('tests/palettes/font1.plt')


if __name__ == '__main__':
    unittest.main()
