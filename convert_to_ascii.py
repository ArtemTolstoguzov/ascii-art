from PIL import Image
import json
import convert_to_binary


def get_size(img, size):
    if size is None:
        w = round(img.size[0] / 8) * 8
        h = round(img.size[1] / 16) * 16
    else:
        w = size[0] * 8
        h = size[1] * 16
    return w, h


def get_palette(palette_name):
    with open(palette_name, 'r') as f:
        return json.load(f)


def get_symbol(cell, palette, inverse):
    pixels = list(cell.getdata())
    cell_codes = []
    for i in range(4):
        code = 0
        for j in pixels[32 * i:32 * (i + 1)]:
            code = code * 10 + j
        cell_codes.append(int(str(code), 2))

    match = -1 if inverse else 129
    match_symbol = ''
    for symbol, symbol_codes in palette.items():
        difference = 0
        for i in range(4):
            difference += bin(symbol_codes[i] ^ cell_codes[i]).count('1')
        if (inverse and difference > match
                or not inverse and difference < match):
            match = difference
            match_symbol = symbol
            if (inverse and match == 128) or (not inverse and match == 0):
                return match_symbol
    return match_symbol


def convert(image, res_size, palette_name, inverse):
    img = Image.open(image)
    size = get_size(img, res_size)
    palette = get_palette(palette_name)
    bin_img = convert_to_binary.get_binary_image(img, size)
    result = []
    for row in range(0, bin_img.size[1], 16):
        line = []
        for column in range(0, bin_img.size[0], 8):
            cell = bin_img.crop((column, row, column + 8, row + 16))
            line.append(get_symbol(cell, palette, inverse))
        result.append(''.join(line))
    return result


if __name__ == '__main__':
    pass
