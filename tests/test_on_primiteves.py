import unittest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
import convert_to_ascii


def cut_top_bottom(ascii):
    top = 0
    bottom = 0
    start = False
    for i, line in enumerate(ascii):
        if not start and ' ' in line:
            top = i
            start = True
        if start and ' ' not in line:
            bottom = i - 1
    return ascii[top:bottom], top, bottom


class ConvertTest(unittest.TestCase):
    def test_on_circle(self):
        ascii = convert_to_ascii.convert(
            'tests/img/primitives/circle.jpg', (20, 10),
            'palettes/UbuntuMono.plt', False)
        ascii = cut_top_bottom(ascii)[0]
        previous = ''
        half = False
        p_diff = 0
        for i in range(len(ascii)):
            p_bs = previous.count(' ')
            c_bs = ascii[i].count(' ')
            c_diff = abs(p_bs - c_bs)
            if not half:
                self.assertLessEqual(p_bs, c_bs)
            else:
                self.assertGreaterEqual(p_bs, c_bs)
            if p_bs == c_bs and previous:
                half = True
            self.assertTrue(p_diff != c_diff or p_diff == 0)
            p_diff = c_diff
            previous = ascii[i]

    def test_on_triangle(self):
        ascii = convert_to_ascii.convert(
            'tests/img/primitives/triangle.jpg', (20, 10),
            'palettes/UbuntuMono.plt', False)
        ascii = cut_top_bottom(ascii)[0]
        previous = ''
        for line in ascii:
            l_bs = line.index(' ')
            r_bs = line.rfind(' ')
            self.assertNotEqual(line[l_bs - 1], ' ')
            self.assertNotEqual(line[r_bs + 1], ' ')
            p_bs = previous.count(' ')
            c_bs = line.count(' ')
            previous = line
            self.assertLessEqual(p_bs, c_bs)

    def test_on_square(self):
        ascii = convert_to_ascii.convert(
            'tests/img/primitives/square.jpg', (20, 10),
            'palettes/UbuntuMono.plt', False)
        ascii, top, bottom = cut_top_bottom(ascii)
        left = ascii[0].index(' ')
        right = ascii[0].rfind(' ')
        for line in ascii:
            l_bs = line[left - 1]
            r_bs = line[right + 1]
            self.assertEqual(l_bs, 'N')
            self.assertEqual(r_bs, 'N')
        self.assertAlmostEqual(2 * (bottom - top), right - left, delta=1)
        ascii = [''.join(line[left:right]) for line in ascii]
        self.assertEqual(''.join(ascii).strip(), '')


if __name__ == '__main__':
    unittest.main()
