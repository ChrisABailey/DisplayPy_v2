DisplayPy.exe

Copyright (c)2022 International Display Consortium
all rights reserved

Display a series of test images for testing LCD performance

usage: DisplayPy.py [-h] [-v | -a | -x | -s | -u | -f]

optional arguments:
  -h, --help        show this help message and exit
  -v, --vga         640x480
  -a, --svga        800x600
  -x, --xga         1024x768
  -s, --sxga        1280x1024
  -u, --uxga        1600x1200
  -f, --fullscreen  fullscreen (default)


When running the following keys display the described test patterns:

f: Flood Fill (cycle R/G/B/W/B) 
	- Displays a full screen of Red when pressed again the display cycles to Green then Blue, White and Black then back to Red.
	- When displaying the flood fill pattern +/- adjusts the greyscale between 0 and 255
a: Animate
	- Displays a screen animation (
b: Color Bars 
	- Displays color bars of White, Yellow, Cyan, Green, Magenta, Red, Blue, Black
g: Color Gradiant 
	- Display 4 bolor bars (Red, Green, Blue and Grey) each increasing from Black to full color (0 to 255)
l: Single Pixel Lines 
	- fills the screen with alternating black and white single pixel lines     
c: Color Test Image 
	- Displays the image named "colorTest.png" in the working directory   
s: Shading Test Image 
	- Displays the image named "greyTest.png" in the working directory
<F11> Toggle FullScreen 
	- toggles between full screen and window mode
<ESC> Exit 
	- Quits the program

