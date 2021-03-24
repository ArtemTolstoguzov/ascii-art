from PIL import Image, ImageDraw, ImageFont
import os
import json
import argparse


def get_symbol_img(symbol, font_path):
    font = ImageFont.truetype(font_path, 16, encoding='ascii')
    img = Image.new('L', font.getsize(symbol), 'black')
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), symbol, 'white', font)
    return img.resize((8, 16))


def get_codes(l_img):
    pixels = list(l_img.getdata())
    pixels = [str(int(p != 0)) for p in pixels]
    codes = [int(''.join(pixels[32 * i:32 * (i + 1)]), 2) for i in range(4)]
    return codes


def convert_to_palette(font_path):
    palette = {chr(i): get_codes(get_symbol_img(chr(i), font_path))
               for i in range(32, 127)}
    return palette


def save_palette(font, palettes_dir):
    palette = convert_to_palette(font)
    font_name = os.path.splitext(os.path.basename(font))[0]
    palette_path = os.path.join(palettes_dir, f'{font_name}.plt')
    with open(palette_path, 'w') as f:
        json.dump(palette, f)


def create_palettes(fonts_dir, palettes_dir):
    if os.path.isdir(fonts_dir):
        if palettes_dir is None:
            palettes_dir = fonts_dir
        for font in os.listdir(fonts_dir):
            save_palette(os.path.join(fonts_dir, font), palettes_dir)
    else:
        if palettes_dir is None:
            palettes_dir = os.path.dirname(fonts_dir)
        save_palette(fonts_dir, palettes_dir)


def get_args():
    arg_parser = argparse.ArgumentParser(
        description='Формирование палитры шрифта')
    arg_parser.add_argument('fonts_dir', type=str,
                            help='Файл шрифта или католог со шрифтами')
    arg_parser.add_argument('palettes_dir', nargs='?',
                            type=str, help='Каталог палитр')
    return arg_parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    create_palettes(args.fonts_dir, args.palettes_dir)
