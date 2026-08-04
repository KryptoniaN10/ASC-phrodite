import sys
class Screen:
    def __init__(self,width,height):
        self.width=width
        self.height=height
        self.buffer=[[" "]*width for _ in range(height)]
    def set_pixel(self,x,y,char):
        if x>=0 and x<self.width and y>=0 and y<self.height:
            self.buffer[y][x]=char
    def render(self):
        sys.stdout.write("\033[H")
        for row in self.buffer:
            sys.stdout.write("".join(row))
            sys.stdout.write("\n")
        sys.stdout.flush()
    def clear_terminal(self):
        sys.stdout.write("\033[2J")
        sys.stdout.flush()
    def clear_buffer(self):
        self.buffer=[[" "]*self.width for _ in range(self.height)]
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