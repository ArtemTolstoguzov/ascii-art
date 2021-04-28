# Ascii-Art
A program to turn images into ASCII-art. It is created by printing characters to your terminal so as to recreate the contours of a source image.
![Screenshot](example.png)

## Usage
```
main.py [-h] [-s width height] [-p PALETTE] [-i] [--interactive] image
```
- positional arguments:
  * `image`

- optional arguments:
  * `-h, --help` : how this help message and exit
  * `-s width height, --size width height` : output image size (in characters)
  * `-p PALETTE, --palette PALETTE` : palette file
  * `-i, --inverse` : invert palette (default: white characters on black)
  * `--interactive` : interactive view of the result

- interactive view commands:
    * Scroll: arrows
    * Zoom: `+`/ `-`
    * Exit: `Q`

## Сreating palettes
```
convert_to_palette.py [-h] fonts_dir [palettes_dir]
```
- positional arguments:
  * `fonts_dir` : font file or fonts directory
  * `palettes_dir` : palette directory

- optional arguments:
  * `-h, --help` : how this help message and exit
