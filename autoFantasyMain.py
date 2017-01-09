import cv2
from PIL import ImageGrab, ImageOps
from numpy import *
import time
import win32api, win32con

#7 down arrows
#xpad y pad adjust for 3 more down arrows
starters = 10
thresh = 1000
hereThresh = 2000
x1 = 782
x2 = 812
xHere1 = 706
xHere2 = 764
xMove = 743
yVal2 = [573, 605, 635, 664, 696, 726, 759, 791, 820, 853, 935, 963, 994, 1024]
yVal3 = [524, 555, 586, 617, 648, 679, 710, 741, 772, 803, 884, 915, 946, 977]
yVal = [564, 595, 626, 657, 688, 719, 750, 781, 812, 843, 924, 955, 986, 1017, 1048, 1079]
util = [7, 8, 9] #one less because array index
x_pad = 6
y_pad = -137
nextDay = (815, 291)
submitCoor = (1365, 444)

def leftClick(c):
    win32api.SetCursorPos((x_pad+c[0],y_pad+c[1]))
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x_pad+c[0],y_pad+c[1])
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x_pad+c[0],y_pad+c[1])
    print("Left click", c[0],c[1])

def grab(c):
    box = (x_pad+c[0] ,y_pad+c[1], x_pad+c[2], y_pad+c[3])
    im = ImageOps.grayscale(ImageGrab.grab(bbox=box))
    a = array(im.getcolors())
    #print("grab", a)
    a = a.sum()
    return a

def getVals():
    a = []
    for y in yVal:
        a.append(grab((x1, y+6, x2, y+14)))
    return a
def getMovVals():
    a = []
    for y in yVal:
        a.append(grab((xHere1, y, xHere2, y+19)))
    return a
def convert(a):
    for x in range(len(a)):
        if a[x]>thresh:
            a[x] = 1
        else:
            a[x] = 0
    return a
def convertH(a):
    for x in range(len(a)):
        if a[x]>hereThresh:
            a[x] = 1
        else:
            a[x] = 0
    return a
def findComp(a):
    #check 0 and 1
    for x in range(0, starters):
        g = grab((xHere1, yVal[x], xHere2, yVal[x]+19))
        print(g)
        if a[x] == 0:
            if g>hereThresh: #check if here is green, idk why the first spot screws up...
                print('found compatible', x, g)
                #ImageGrab.grab((xHere1, yVal[x], xHere2, yVal[x]+2)).save('tempPics\\screenFantasyMove.png', 'PNG')
                #img = cv2.imread('tempPics\\screenFantasyMove.png')
                #cv2.imshow('output', img)
                #cv2.waitKey(0)
                #debug()
                return x
    return -1 #found no suitable swaps

def submit():
    leftClick(submitCoor)

def debug():
    ImageGrab.grab().save('tempPics\\screenFantasy.png', 'PNG')
    img = cv2.imread('tempPics\\screenFantasy.png')
    for y in yVal:
        cv2.rectangle(img, (x_pad+x1, y_pad+y+6), (x_pad+x2, y_pad+y+14), (0, 255, 0))
        cv2.rectangle(img, (x_pad+xHere1, y_pad+y), (x_pad+xHere2, y_pad+y+19), (255, 0, 0))
    cv2.circle(img, (x_pad+nextDay[0], y_pad+nextDay[1]), 3, (255, 0, 0))
    cv2.circle(img, (x_pad+submitCoor[0], y_pad+submitCoor[1]), 3, (255, 0, 0))
    cv2.circle(img, (x_pad+xMove, y_pad+yVal[0]+10), 3, (255, 255, 0))
    cv2.imshow('output', img)
    cv2.waitKey(0)

def main():
    print("Hold LEFT SHIFT to quit")
    for day in range(100):
        print("##############NEW DAY##############")
        if (win32api.GetAsyncKeyState(win32con.VK_LSHIFT)!=0):
            print("Quitting...")
            break
        time.sleep(1) #to wait for browser to load
        a = getVals()
        print(a)
        print("available", convert(a))
        success = 0
        for x in range(starters, len(a)):
            if a[x]==1:
                success-=1
                print("bench ", x+1, " needs moving")
                leftClick((xMove, yVal[x]))
                time.sleep(0.1)
                g = getMovVals()
                print("green values", g)
                print(convertH(g))
                #debug()
                f = findComp(a)
                print("swapping with ", f)
                if f!=-1: #actually swapping
                    success+=1
                    leftClick((xMove, yVal[f]+10))
                    a[x]=0
                    a[f]=1
                    print("new ", a)
                else: #not swapping
                    leftClick((xMove, yVal[x]))
        submit()
        print('Today was a ', success==0)
        #debug()
        time.sleep(0.1)
        leftClick(nextDay)
def mainDebug():
    print(getVals())
    print(getMovVals())
if __name__ == '__main__':
    main()