import sys
import shutil

try:
    import colorama
    colorama.just_fix_windows_console()
except Exception:
    pass

# Reconfigure stdout to use UTF-8 to support Unicode shading blocks (░▒▓█) on all terminals
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

_COLOR_CACHE = {}

class Screen:
    def __init__(self,width,height):
        self.width=width
        self.height=height
        self.buffer = [[(" ", None) for _ in range(width)] for _ in range(height)]

    def update_size(self):
        # Query current terminal size and update buffer if changed
        size = shutil.get_terminal_size(fallback=(self.width, self.height))
        cols, lines = size.columns, size.lines
        # Leave a 1-row safety margin at the bottom to prevent terminal scrolling
        target_height = max(1, lines - 1)
        if cols != self.width or target_height != self.height:
            self.width = cols
            self.height = target_height
            self.buffer = [[(" ", None) for _ in range(self.width)] for _ in range(self.height)]
    def set_pixel(self,x,y,char,color=None):
        if x>=0 and x<self.width and y>=0 and y<self.height:
            self.buffer[y][x]=(char,color)
    def render(self):
        # Move cursor to home
        chunks = ["\033[H"]
        last_color = None
        color_cache = _COLOR_CACHE
        for i, row in enumerate(self.buffer):
            for char, color in row:
                if color != last_color:
                    if color is None:
                        chunks.append("\033[0m")
                    else:
                        ansi_code = color_cache.get(color)
                        if ansi_code is None:
                            ansi_code = f"\033[38;2;{color[0]};{color[1]};{color[2]}m"
                            color_cache[color] = ansi_code
                        chunks.append(ansi_code)
                    last_color = color
                chunks.append(char)
            if i < len(self.buffer) - 1:
                chunks.append("\n")
        if last_color is not None:
            chunks.append("\033[0m")
        # Clear any remaining lines below the rendered area
        chunks.append("\033[J")
        sys.stdout.write("".join(chunks))
        sys.stdout.flush()
    def clear_terminal(self):
        # Clear entire screen and move cursor to home
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
    def clear_buffer(self):
        self.buffer = [[(" ", None) for _ in range(self.width)] for _ in range(self.height)]
    def draw_horizontal_line(self,x1,x2,y,char):
        for i in range(x1,x2+1):
            self.set_pixel(i,y,char)
    def draw_vertical_line(self,x,y1,y2,char):
            for i in range(y1,y2+1):
                self.set_pixel(x,i,char)
    def draw_rectangle(self,x1,y1,width,height,char):
        self.draw_vertical_line(x1,y1,y1+height-1,char)
        self.draw_horizontal_line(x1,x1+width-1,y1,char)
        self.draw_vertical_line(x1+width-1,y1,y1+height-1,char)
        self.draw_horizontal_line(x1,x1+width-1,y1+height-1,char)