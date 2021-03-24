import curses
import argparse
import convert_to_ascii


class Display:
    def __init__(self, content):
        self.screen = curses.initscr()
        curses.cbreak()
        curses.noecho()
        curses.curs_set(False)
        self.max_y = len(content)
        self.max_x = len(content[0]) + 1
        self.pad = curses.newpad(self.max_y, self.max_x)
        self.pad.keypad(True)
        for i in range(len(content)):
            self.pad.addstr(i, 0, content[i])
        self.current_y = 0
        self.current_x = 0
        self.refresh_pad()

    def refresh_pad(self):
        height, width = self.screen.getmaxyx()
        height = min(height, self.max_y)
        width = min(width, self.max_x)
        if self.current_y < 0:
            self.current_y = 0
        if self.current_x < 0:
            self.current_x = 0
        if self.current_y + height > self.max_y:
            self.current_y = self.max_y - height
        if self.current_x + width > self.max_x:
            self.current_x = self.max_x - width
        self.screen.clear()
        self.pad.refresh(
            self.current_y, self.current_x, 0, 0, height - 1, width - 1)

    def zoom(self, ch, step=0.1):
        kf = 1 - step if ch == ord('-') else 1 / (1 - step)
        self.screen.clear()
        self.screen.addstr(0, 0, 'loading...')
        self.screen.refresh()
        content = convert_to_ascii.convert(
            args.image.name,
            (int((self.max_x - 1) * kf), int(self.max_y * kf)),
            args.palette, args.inverse)
        self.max_y = len(content)
        self.max_x = len(content[0]) + 1
        self.pad.resize(self.max_y, self.max_x)
        for i in range(len(content)):
            self.pad.addstr(i, 0, content[i])
        self.current_y = 0
        self.current_x = 0
        self.refresh_pad()

    def show(self):
        while True:
            ch = self.pad.getch()

            if ch == curses.KEY_UP:
                self.current_y -= 1
            if ch == curses.KEY_DOWN:
                self.current_y += 1
            if ch == curses.KEY_LEFT:
                self.current_x -= 1
            if ch == curses.KEY_RIGHT:
                self.current_x += 1

            if ch == ord('-') or ch == ord('+'):
                self.zoom(ch)

            if ch == ord('q') or ch == ord('Q'):
                self.end_show()
                break

            self.refresh_pad()

    def end_show(self):
        curses.nocbreak()
        curses.echo()
        curses.curs_set(True)
        self.pad.keypad(False)
        curses.endwin()


def get_args():
    arg_parser = argparse.ArgumentParser(
        description='Конвертирование цветного изображения в ASCII-art')
    arg_parser.add_argument('image', type=argparse.FileType(),
                            help='Изображение')
    arg_parser.add_argument('-s', '--size', type=int, nargs=2, action='store',
                            metavar=('width', 'height'),
                            help='Размер выходного изображения(в символах)')
    arg_parser.add_argument('-p', '--palette', type=str, help='Файл палитры',
                            default='palettes/UbuntuMono.plt')
    arg_parser.add_argument('-i', '--inverse', action='store_true',
                            help='Инверсия палитры(по умолчанию: белые символы'
                                 ' на черном фоне)')
    arg_parser.add_argument('--interactive', action='store_true',
                            help='Интерактивный просмотр результата')
    return arg_parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    ascii = convert_to_ascii.convert(args.image.name, args.size,
                                     args.palette, args.inverse)
    if args.interactive:
        Display(ascii).show()
    else:
        for line in ascii:
            print(line)
