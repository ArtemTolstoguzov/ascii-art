from PIL import Image
import unittest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
import convert_to_ascii


class FuncTest(unittest.TestCase):
    def test_get_default_size(self):
        img = Image.open('tests/img/default.jpg')
        size = convert_to_ascii.get_size(img, None)
        img.close()
        self.assertEqual(size[0] % 8, 0)
        self.assertEqual(size[1] % 16, 0)

    def test_get_symbol_size(self):
        img = Image.open('tests/img/default.jpg')
        size = convert_to_ascii.get_size(img, (20, 10))
        img.close()
        self.assertEqual(size[0] / 8, 20)
        self.assertEqual(size[1] / 16, 10)

    def test_get_palette(self):
        palette = convert_to_ascii.get_palette('palettes/UbuntuMono.plt')
        self.assertTrue(len(palette) == 95)
        for symbol in palette:
            self.assertEqual(len(palette[symbol]), 4)


if __name__ == '__main__':
    unittest.main()
