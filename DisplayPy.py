#!/usr/bin/python
import math
from operator import truediv
import tkinter as tk
# pip install pillow
# apt-get install python3-pil.imagetk
from PIL import Image, ImageTk
import argparse
import sys
import os
import numpy as np
#pip install screeninfo
from screeninfo import get_monitors

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

# def rgb(npy array[r,g,b]):
#   return "#%s%s%s" % tuple([hex(c)[2:].rjust(2, "0")
#	  for c in (r, g, b)])
def rgb(color):
    return "#%s%s%s" % tuple([hex(c)[2:].rjust(2, "0") for c in color])


class App(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)

        self.window = parent

        self.initUI()

    def initUI(self):

        self.window.title("Display Test")

        self.pack(fill="both", expand=True, side="top")

        #self.window.wm_state("zoomed")
        #self.window.attributes('-zoomed', True)

        self.fullScreenState = False

        self.window.bind("<F12>", self.fullscreen_cancel)
        self.window.bind("<F11>", self.fullscreen_toggle)
        self.window.bind("<Escape>", self.close)
        self.window.bind('s', self.shadeImage)
        self.window.bind('a', self.startAnimate)
        self.window.bind('b', self.colorBars)
        self.window.bind('l', self.displayLines)
        self.window.bind('g', self.colorGradiants)
        self.window.bind('c', self.colorImage)
        self.window.bind('h', self.displayHelp)
        self.window.bind('?', self.displayHelp)
        self.window.bind('f', self.floodFill)
        self.window.bind('+', self.greyUp)
        self.window.bind('-', self.greyDown)

        # Screen Width and Height
        for m in get_monitors():
           if (m.is_primary):
               self.ws1 = m.width
               self.hs1 = m.height
           else:
               self.ws2 = m.width
               self.hs2 = m.height

        if (args.xga):
            self.sx = 1024
            self.sy = 768
        elif (args.svga):
            self.sx = 800
            self.sy = 600
        elif (args.vga):
            self.sx = 640
            self.sy = 480
        elif (args.sxga):
            self.sx = 1280
            self.sy = 1024     
        elif (args.uxga):
            self.sx = 1600
            self.sy = 1200   
        elif (args.lad):
            self.sx = 2560
            self.sy = 1024             
        else: #fullscreen
            #this returns the size of both windows in multi monitor Linux
            #self.sx = self.window.winfo_screenwidth()
            #self.sy = self.window.winfo_screenheight()
            if(args.second):
                self.sx=self.ws2
                self.sy=self.hs2
            else:
                self.sx=self.ws1
                self.sy=self.hs1

        if (self.sx<self.sy):  # portrait orientation
            self.portrait = True
        else:
            self.portrait = False
        self.fullscreen_toggle()



        #self.label = tk.Label(self, text="Fullscreen", font=("default",120), fg="black")
        #self.label.pack(side="top", fill="both", expand=True)

        #self.primaries = ['red','green','blue','white','black']
        self.primaries = [[1, 0, 0], [0, 1, 0],
                          [0, 0, 1], [1, 1, 1], [0, 0, 0]]
        self.currentColorIndex = 0
        self.TestScreens = ['help', 'shade',
                            'bars', 'gradiants', 'color', 'flood','lines','animate']
        self.currentTestScreen = self.TestScreens.index('help')
        # this is used in the flood field screen
        self.currentGreyscale = 255
        self.currentStep=0


        self.canvas = tk.Canvas(
            self.window, width=self.sx, height=self.sy, bg='black', bd=0, highlightthickness=0)
        self.canvas.place(x=0, y=0)

        self.drawHelp()

    def fullscreen_toggle(self, event="none"):

        self.fullScreenState = not self.fullScreenState
        w,h = self.window.winfo_screenwidth(),self.window.winfo_screenheight()
        self.window.focus_set()
        if (self.fullScreenState):
            if (args.second):
            	# the following line puts this on screen 2 always
            	geo = ('%sx%s+%d+%d'%(self.sx,self.sy,self.ws1,0))
            	self.window.geometry(geo)
            else:
                # following line puts the screen on Screen 1 always
                self.window.geometry('%sx%s+%d+%d'%(self.ws1,self.hs1,0,0))

        # self.window.overrideredirect(True)
        # self.window.overrideredirect(False) #added for a toggle effect, not fully sure why it's like this on Mac OS
        self.window.attributes("-fullscreen", self.fullScreenState)
        self.window.wm_attributes("-topmost", self.fullScreenState)
        if (not self.fullScreenState):
            self.window.geometry("%dx%d+0+0" % (self.sx*4/5, self.sy*4/5))

    def fullscreen_cancel(self, event="none"):

        self.window.overrideredirect(False)
        self.window.attributes("-fullscreen", False)
        self.window.wm_attributes("-topmost", 0)

        self.centerWindow()

    def centerWindow(self):

        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()

        w = sw*0.7
        h = sh*0.7

        x = (sw-w)/2
        y = (sh-h)/2

        self.window.geometry("%dx%d+%d+%d" % (w, h, x, y))

    def showImage(self, filename):
        self.canvas.delete('all')
        img = Image.open(filename)
        if not hasattr(Image, 'Resampling'):  # Pillow<9.0
            Image.Resampling = Image
        self.image2 = ImageTk.PhotoImage(img.resize(
            (self.sx, self.sy), Image.Resampling.LANCZOS))
        #self.image2.resize((self.sx, self.sy), Image.Resampling.LANCZOS)
        self.canvas.create_image(0, 0, image=self.image2, anchor='nw')

    def close(self, event):
        self.window.destroy()

    def shadeImage(self, event):
        full_path = os.path.join(application_path, "greyTest.png")
        self.currentTestScreen = self.TestScreens.index('shade')
        self.showImage(full_path)

    def colorImage(self, event):
        full_path = os.path.join(application_path, "colorTest.png")
        self.currentTestScreen = self.TestScreens.index('color')
        self.showImage(full_path)
        
    def greyUp(self,event):
        self.currentGreyscale = (self.currentGreyscale + 1)%255
        if self.currentTestScreen == self.TestScreens.index('flood'):
            self.canvas.configure(bg=rgb(np.multiply(
                self.primaries[self.currentColorIndex], self.currentGreyscale)))
            self.canvas.itemconfig(self.bg1,text="%d"%self.currentGreyscale) 
            self.canvas.itemconfig(self.bg2,text="%d"%self.currentGreyscale)    
            self.canvas.itemconfig(self.bg3,text="%d"%self.currentGreyscale)
            self.canvas.itemconfig(self.bg4,text="%d"%self.currentGreyscale)
            self.canvas.itemconfig(self.fg,text="%d"%self.currentGreyscale) 

    def greyDown(self,event):
        self.currentGreyscale = self.currentGreyscale-1 if (self.currentGreyscale > 1) else 255
        if self.currentTestScreen == self.TestScreens.index('flood'):  
            self.canvas.configure(bg=rgb(np.multiply(
                self.primaries[self.currentColorIndex], self.currentGreyscale)))
            self.canvas.itemconfig(self.bg1,text="%d"%self.currentGreyscale) 
            self.canvas.itemconfig(self.bg2,text="%d"%self.currentGreyscale)    
            self.canvas.itemconfig(self.bg3,text="%d"%self.currentGreyscale)
            self.canvas.itemconfig(self.bg4,text="%d"%self.currentGreyscale)
            self.canvas.itemconfig(self.fg,text="%d"%self.currentGreyscale)       

    def floodFill(self, event):
        if self.currentTestScreen != self.TestScreens.index('flood'):
            self.currentColorIndex = 0
            self.currentGreyscale = 255
        else:
            self.currentColorIndex = (self.currentColorIndex+1) % 5
        self.currentTestScreen = self.TestScreens.index('flood')
        self.canvas.delete('all')
        self.canvas.configure(bg=rgb(np.multiply(
            self.primaries[self.currentColorIndex], self.currentGreyscale)))
        if not self.portrait:
            lx = 30
            ly=750
            angle=90
        else:
            lx=30
            ly=30
            angle=0
        self.bg1 = self.canvas.create_text(
            lx+1, ly+1, text="%d"%self.currentGreyscale, anchor="nw", fill='black',font='helvetica 12', angle=angle)
        self.bg2 = self.canvas.create_text(
            lx-1, ly+1, text="%d"%self.currentGreyscale, anchor="nw", fill='black',font='helvetica 12', angle=angle)   
        self.bg3 = self.canvas.create_text(
            lx+1, ly-1, text="%d"%self.currentGreyscale, anchor="nw", fill='black',font='helvetica 12', angle=angle)
        self.bg4 = self.canvas.create_text(
            lx-1, ly-1, text="%d"%self.currentGreyscale, anchor="nw", fill='black',font='helvetica 12', angle=angle) 
        self.fg = self.canvas.create_text(
            lx, ly, text="%d"%self.currentGreyscale, anchor="nw", fill='white',font='helvetica 12', angle=angle)
        

    def colorBars(self, event):
        self.currentTestScreen = self.TestScreens.index('bars')
        self.canvas.delete('all')
        for i, color in enumerate(['#FFFFFF', '#FFFF00','#00FFFF', '#00FF00','#FF00FF','#FF0000', '#0000FF','#000000']):
            self.canvas.create_rectangle(
                i*(self.sx/8), -1, (i+1)*(self.sx/8), self.sy+1, fill=color, outline=color)

    def colorGradiants(self, event):    
        self.currentTestScreen = self.TestScreens.index('gradiants')
        self.canvas.delete('all')
        xstep = self.sx/256.0
        ystep = self.sy/4.0
        for i in range(0, 256):
            self.canvas.create_rectangle(
                i * xstep, 0, (i+1)*xstep, ystep, fill=rgb([i, 0, 0]), outline=rgb([i, 0, 0]))
            self.canvas.create_rectangle(
                i * xstep, ystep, (i+1)*xstep, ystep*2, fill=rgb([0, i, 0]), outline=rgb([0, i, 0]))
            self.canvas.create_rectangle(
                i * xstep, ystep*2, (i+1)*xstep, ystep*3, fill=rgb([0, 0, i]), outline=rgb([0, 0, i]))
            self.canvas.create_rectangle(
                i * xstep, ystep*3, (i+1)*xstep, ystep*4, fill=rgb([i, i, i]), outline=rgb([i, i, i]))

    def displayLines(self, event):
        self.currentTestScreen = self.TestScreens.index('lines')
        self.canvas.delete('all')
        self.canvas.configure(bg='black')
        for i in range(0,self.sx,2):
            self.canvas.create_line(i,0,i,self.sy,fill='#FFFFFF',width=1)

    def displayHelp(self, event):
        self.currentTestScreen = self.TestScreens.index('help')
        self.drawHelp()

    def startAnimate(self,event):
        self.currentTestScreen = self.TestScreens.index('animate')
        self.animate()

    def getPoint(self,step):
        r=.5*self.sy*math.cos(10*step/400)
        x1=self.sx/2 + r*1.33 * math.cos(step/400)
        y1=self.sy/2 +r * math.sin(step/400) 
        return x1, y1
 
    def animate(self):
        if (self.currentTestScreen != self.TestScreens.index('animate')):
            return

        self.canvas.delete('all')
        step = self.currentStep
        self.canvas.configure(bg=rgb([step//7%255,(step//3)%255,(step//11)%255]))
        x1, y1 =self.getPoint(step - 25)
        x2, y2 =self.getPoint(step - 20)
        self.canvas.create_line(
            x1, y1, x2, y2,fill='#FFFFFF',width=2)
        self.canvas.create_oval(x2-5,y2-5,x2+5,y2+5,fill='#FFFFFF')
        x1, y1 =self.getPoint(step - 15)
        self.canvas.create_line(
            x2, y2, x1, y1,fill='#FFFFFF',width=3)
        self.canvas.create_oval(x1-10,y1-10,x1+10,y1+10,fill='#FFFFFF',width=2)
        x2, y2 =self.getPoint(step - 10)
        self.canvas.create_line(
            x1, y1, x2, y2,fill='#FFFFFF',width=4)  
        self.canvas.create_oval(x2-15,y2-15,x2+15,y2+15,fill='#FFFFFF',width=3)                  
        x1, y1 =self.getPoint(step)
        self.canvas.create_line(
            x2, y2, x1, y1,fill='#FFFFFF',width=5)        
        self.canvas.create_oval(x1-20,y1-20,x1+20,y1+20,fill='#FFFFFF',width=4)

        self.currentStep+=1
            
        # schedule timer to call myself after .032 seconds
        self.after(32, self.animate)

    def drawHelp(self):
        self.canvas.delete('all')
        self.helpText = """DisplayTest ({},{}):
    f: Flood Fill (each press cycles R/G/B/W/Bk)
    +/-: Change Fill Greyshade
    a: Animation
    b: Color Bars
    g: Color Gradiant
    l: Single Pixel Lines
    c: Color Test Image
    s: Shading Test Image
    <F11> Toggle FullScreen
    <ESC> Exit""".format(self.sx,self.sy)
        self.canvas.create_rectangle(
            0, 0, self.sx-1, self.sy-1, outline='white', fill='black')
        if not self.portrait:
            self.help = self.canvas.create_text(
                100, self.sy*.9, text=self.helpText, anchor="nw", fill='white', font='helvetica 18', angle=90)
        else:
            self.help = self.canvas.create_text(
                self.sx*.1,self.sy*.1, text=self.helpText, anchor="nw", fill='white', font='helvetica 18')



if __name__ == "__main__":

    global args
    parser = argparse.ArgumentParser()

    # Adding optional argument
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--vga", help = "640x480",action='store_true') 
    group.add_argument("-a", "--svga", help = "800x600",action='store_true')     
    group.add_argument("-x", "--xga", help = "1024x768",action='store_true') 
    group.add_argument("-s", "--sxga", help = "1280x1024",action='store_true') 
    group.add_argument("-u", "--uxga", help = "1600x1200",action='store_true') 
    group.add_argument("-l", "--lad", help = "2560x1024",action='store_true') 
    group.add_argument("-f", "--fullscreen", help = "fullscreen (default)",action='store_true') 
    parser.add_argument("-2","--second", help= "second Screen", action='store_true')
    args = parser.parse_args()
 
    
    root = tk.Tk()
    App(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
