from PIL import Image
import unittest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
import convert_to_binary as ctb


class ConvertTest(unittest.TestCase):
    def test_get_cdf(self):
        l_img = Image.open('tests/img/to_binary/hands.jpg').convert('L')
        self.assertEqual(
            l_img.size[0] * l_img.size[0], ctb.get_cdf(l_img)[255])

    def test_get_gray_scale_img(self):
        img = Image.open('tests/img/to_binary/road.jpg')
        l_img = ctb.get_gray_scale_img(img)
        for x in range(l_img.size[0]):
            for y in range(l_img.size[1]):
                p = l_img.getpixel((x, y))
                self.assertTrue(0 <= p <= 255)

    def test_stretch_and_normalize_histogram(self):
        l_img = Image.open('tests/img/to_binary/jer.jpg').convert('L')
        self.assertEqual(l_img.histogram()[0], 0)
        ctb.stretch_and_normalize_histogram(l_img)
        self.assertNotEqual(l_img.histogram()[0], 0)
        self.assertNotEqual(l_img.histogram()[255], 0)

    def test_equalize_histogram(self):
        imgs = ['road', 'forest']
        for img in imgs:
            l_img = Image.open(f'tests/img/to_binary/{img}.jpg').convert('L')
            ctb.stretch_and_normalize_histogram(l_img)
            ctb.equalize_histogram(l_img)
            cdf = ctb.get_cdf(l_img)
            ratio = cdf[255] / 255
            delta = cdf[255] * 0.01
            for i in range(0, 255, 16):
                expected = round(i * ratio)
                self.assertAlmostEqual(expected, cdf[i], delta=delta)

    def test_change_contrast(self):
        l_img = Image.open('tests/img/to_binary/forest.jpg').convert('L')
        old_scope = (l_img.histogram()[0], l_img.histogram()[255])
        ctb.change_contrast(l_img)
        new_scope = (l_img.histogram()[0], l_img.histogram()[255])
        self.assertGreater(new_scope[0], old_scope[0])
        self.assertGreater(new_scope[1], old_scope[1])

    def test_binarize(self):
        l_img = Image.open('tests/img/to_binary/hands.jpg').convert('L')
        ctb.binarize(l_img)
        self.assertEqual(l_img.histogram()[0] + l_img.histogram()[1],
                         ctb.get_cdf(l_img)[255])

    def test_get_binary_image(self):
        l_img = Image.open('tests/img/to_binary/jer.jpg')
        size = (300, 300)
        b_img = ctb.get_binary_image(l_img, size)
        self.assertTupleEqual(size, b_img.size)


if __name__ == '__main__':
    unittest.main()
