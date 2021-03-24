from PIL import Image
import math


def get_cdf(l_img):
    cdf = [0 for _ in range(256)]
    histogram = l_img.histogram()
    cdf[0] = histogram[0]
    for i in range(1, 256):
        cdf[i] = cdf[i - 1] + histogram[i]
    return cdf


def get_gray_scale_img(img):
    l_img = Image.new('L', img.size)
    for x in range(l_img.size[0]):
        for y in range(l_img.size[1]):
            rgb = img.getpixel((x, y))
            p = round(rgb[0] * 0.299 + rgb[1] * 0.587 + rgb[2] * 0.114)
            l_img.putpixel((x, y), p)
    return l_img


def stretch_and_normalize_histogram(l_img, indent=0.05):
    min_index = 256
    max_index = -1
    cdf = get_cdf(l_img)
    indent_in_pixels = cdf[255] * indent
    for i in range(256):
        if cdf[i] > indent_in_pixels and i < min_index:
            min_index = i
        if cdf[255] - cdf[i] > indent_in_pixels:
            max_index = i

    ratio = 255 / (max_index - min_index)

    for x in range(l_img.size[0]):
        for y in range(l_img.size[1]):
            p = round(ratio * (l_img.getpixel((x, y)) - min_index))
            l_img.putpixel((x, y), p)


def equalize_histogram(l_img):
    cdf = get_cdf(l_img)
    amount = cdf[255]
    for x in range(l_img.size[0]):
        for y in range(l_img.size[1]):
            p = round(cdf[l_img.getpixel((x, y))] / (amount - 1) * 255)
            l_img.putpixel((x, y), p)


def change_contrast(l_img):
    for x in range(l_img.size[0]):
        for y in range(l_img.size[1]):
            p = round((-math.cos(math.pi * l_img.getpixel((x, y))
                                 / 255) + 1) / 2 * 255)
            l_img.putpixel((x, y), p)


def binarize(l_img):
    for x in range(l_img.size[0]):
        for y in range(l_img.size[1]):
            p = 0 if l_img.getpixel((x, y)) < 128 else 1
            l_img.putpixel((x, y), p)


def get_binary_image(img, size):
    r_img = img.resize(size)
    l_img = get_gray_scale_img(r_img)
    stretch_and_normalize_histogram(l_img)
    histogram = l_img.histogram()
    if abs(255 - histogram.index(max(histogram))) > 5:
        equalize_histogram(l_img)
    change_contrast(l_img)
    binarize(l_img)
    return l_img


if __name__ == '__main__':
    pass
