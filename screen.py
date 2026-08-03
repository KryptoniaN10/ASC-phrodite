import time
import sys
class Screen:
    def __init__(self,width,height):
        self.width=width
        self.height=height
        self.buffer=[[" "]*width for _ in range(height)]
    def set(self,x,y,char):
        self.buffer[y][x]=char
    def render(self):
        sys.stdout.write("\033[H")
        for row in self.buffer:
            sys.stdout.write("".join(row))
        sys.stdout.flush()
    def clear(self):
        sys.stdout.write("\33[2J")

screen1=Screen(5,5)
screen1.clear()
screen1.set(2,3,'@')
screen1.render()
time.sleep(3)
screen1.set(1,1,"#")
screen1.render()