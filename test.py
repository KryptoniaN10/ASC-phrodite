import sys
import time

progress=0
while(progress<21):
    sys.stdout.write("\r")
    sys.stdout.write("[")
    for i in range(20):
        if i<progress:
            sys.stdout.write("#")
        else:
            sys.stdout.write("-")
    sys.stdout.write("]")
    sys.stdout.write(str((progress/20)*100)+"%")
    sys.stdout.flush()
    time.sleep(0.25)
    progress+=1
    