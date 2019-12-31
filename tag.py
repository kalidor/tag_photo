#!/usr/bin/env python3.8
# Encoding: utf-8
# License: WTFPL (https://fr.wikipedia.org/wiki/WTFPL)

# Libraries import
import tkinter as tk
from tkinter.filedialog import askdirectory
from PIL import Image, ImageTk
import os, sys, subprocess, argparse
import time

# Variables declaration
current_img = ""
reservetable = {
    "clear"  : "01",
    "gray"   : "03",
    "green"  : "04",
    "purple" : "06",
    "blue"   : "09",
    "yellow" : "0A",
    "red"    : "0C",
    "orange" : "0E",
    "c"      : "01",
    "a"      : "03",
    "g"      : "04",
    "p"      : "06",
    "b"      : "09",
    "y"      : "0A",
    "r"      : "0C",
    "o"      : "0E",
}
colors_available = reservetable.keys()

plist = '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"><plist version="1.0"><array>{}</array></plist>'

plists = []

# Generate plist XML tag
def gen_plist(color, tagname):
    print('[+] Gen plist for color <{}> and tagname <{}>'.format(color, tagname))
    return plist.format('<string>{}</string>'.format(tagname))


# Use global var to get current_img, kind ugly
# Write tag name and tag color for the current_file
# This function is binding to a key
# Event var is not used
def add_tag(event, tagname, color):
    global current_img
    global directory
    path = (os.path.join(directory, current_img))
    # returns output as byte string

    tag = gen_plist(color, tagname)
    returned_output = subprocess.check_output(
    ["xattr","-w", "com.apple.metadata:_kMDItemUserTags", tag, path]
    )
    #print(returned_output)
    c = "0" * 18 + reservetable[color] + "0" * 44
    returned_output = subprocess.check_output(
    ["xattr","-wx","com.apple.FinderInfo", c, path]
    )
    #print(returned_output)
    print('[+] {} tagged as {}'.format(path, tagname))

# This function is binding to Enter key and call next_img()
# Event var is not used
def next_(event):
    global current_img
    next_img()

# Function to load the next image into the Label
def next_img():
    global current_img
    print('- NEXT_IMG')
    #img_label.img = ImageTk.PhotoImage(file=next(imgs))
    current_img = next(imgs)
    print(current_img)
    image = Image.open(current_img)
    image = image.resize((250, 250), Image.ANTIALIAS) ## The (250, 250) is (height, width)
    img_label.img = ImageTk.PhotoImage(image)
    img_label.config(image=img_label.img)


# Parser declaration
parser = argparse.ArgumentParser()
parser.add_argument('-t', action="extend", nargs="+", type=str, help='color:tagname:letter')
parser.add_argument('directory')
args = parser.parse_args()

if not args.directory:
    print(parser.help)
    sys.exit(0)

if not args.t:
    print('[-] No color given')
    print('[i] Available colors:')
    for i in colors_available:
        print('  {}'.format(i))
    print(parser.format_help())
    sys.exit(0)

directory = args.directory
print('[+] Directory {}'.format(directory))

for elm in args.t:
    color, tag, letter = elm.split(':')
root = tk.Tk()

# Choose multiple images
#directory = askdirectory(parent=root, initialdir="/Users/kalidor/Desktop/NZ_PHOTOWEB", title='Choose folder')
os.chdir(directory)
imgs = iter(os.listdir(directory))

img_label = tk.Label(root)
img_label.pack()

current_img = list(os.listdir(directory))[0] # load first image
next_img()

# Dynamically bind given key to given tagname and given color
# The expected format is "color:tagname:letter"
for elm in args.t:
    color, tagname, letter = elm.split(':')
    # thanks stackoverflow
    # https://stackoverflow.com/questions/14259072/tkinter-bind-function-with-variable-in-a-loop
    def make_lambda(tagname, color):
        return lambda ev:add_tag(None, tagname, color)
    print('[+] Creating binding for letter <{}>: <{}>'.format(letter, color))
    root.bind("<{}>".format(letter), make_lambda(tagname, color))

# Enter will call next_ function and display the next image
root.bind("<Return>", next_)

# Maybe useless button here...
btn = tk.Button(root, text='Next image', command=next_img)
btn.pack(side='top')

# Tkinter loop
root.mainloop()
