__author__ = 'Inschato'
'''
Some Code borrowed from the Rebirth Item Tracker:
https://github.com/Hyphen-ated/RebirthItemTracker/

Copyright (c) 2015, Brett824 and Hyphen-ated
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import os
import json
from Tkinter import *
from PIL import Image, ImageTk
import ttk
from random import sample, seed

valid_items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21, 27, 28, 32, 46, 48, 50, 51, 52, 53,
               54, 55, 57, 60, 62, 63, 64, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 79, 80, 81, 82, 87, 88, 89, 90, 91,
               94, 95, 96, 98, 99, 100, 101, 103, 104, 106, 108, 109, 110, 112, 113, 114, 115, 116, 117, 118, 120, 121,
               122, 125, 128, 129, 131, 132, 134, 138, 139, 140, 141, 142, 143, 144, 148, 149, 150, 151, 152, 153, 154,
               155, 156, 157, 159, 161, 162, 163, 165, 167, 168, 169, 170, 172, 173, 174, 178, 179, 180, 182, 183, 184,
               185, 187, 188, 189, 190, 191, 193, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208,
               209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 227, 228, 229, 230,
               231, 232, 233, 234, 236, 237, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 254, 255,
               256, 257, 258, 259, 260, 261, 262, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277,
               278, 279, 280, 281, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315,
               316, 317, 318, 319, 320, 321, 322, 327, 328, 329, 330, 331, 332, 333, 335, 336, 337, 340, 341, 342, 343,
               345]


class SeedFind:
    """
    Class for finding seeds with specified items, or finding the items of a specific seed
    """

    def __init__(self, window):
        self.valid_items = valid_items
        self.window = window
        with open("items.txt", "r") as f:
            self.items_info = json.load(f)

    def getItemList(self, rngSeed):
        seed(str(rngSeed))
        # creates list of 33 unique items from the valid items list
        return sample(self.valid_items, 33)

    def getSeed(self, desiredSeed):
        chars = [0] * 11
        itemIDs = self.getItemList(desiredSeed)
        for i in range(0, 11):
            chars[i] = itemIDs[3 * i:(3 * i) + 3]
        return chars

    # Redefine me to redirect this output
    def seedOut(self, number, character, items):
        pass

    def findSeeds(self, desiredID, instances=1, offset=0, character=11):
        for ID in desiredID:
            if ID not in self.valid_items:
                print("Error, item(s) not in valid_items list.")
                self.window.window.destroy()
                return None
        nextSeed = offset
        desiredID = frozenset(desiredID)
        seedsFound = 0
        result = []
        chars = [0] * 11
        while True:
            if nextSeed % 1024:
                try:
                    self.window.window.update()
                except:
                    return
            itemIDs = self.getItemList(nextSeed)
            if character == 11:
                for i in range(0, 11):
                    chars[i] = itemIDs[3 * i:(3 * i) + 3]
            else:
                chars = [itemIDs[3 * character:(3 * character) + 3]]
            for i, char in enumerate(chars):
                if not (desiredID <= set(char)):
                    continue
                result += [nextSeed]
                seedsFound += 1
                self.seedOut(nextSeed, i if character == 11 else character, char)
                if seedsFound >= instances:
                    return result
            nextSeed += 1




class SeedsDisplay:
    """
    Class for displaying lists of seeds using character and item images
    """
    def __init__(self, parent=None):
        self.row = 0
        self._image_library = {}
        with open("items.txt", "r") as f:
            self.items_info = json.load(f)
        self.valid_items = valid_items

        # Initialize the window
        self.window = Toplevel(parent) if parent else Tk()
        self.window.configure(background="#191919")
        self.window.title("Seed Viewer")
        self.window.resizable(0, 1)

        # Initialize the scrolling canvas
        self.canvas = Canvas(self.window, background="#191919", borderwidth=0)
        self.scrollbar = Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=200, height=200)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.imageBox = LabelFrame(self.canvas, background="#191919", foreground="#FF0000", borderwidth=0)
        self.loadingMsg = Label(self.imageBox, text="Loading..", background="#191919", foreground="#FFFFFF",
                                font=("Helvetica", 16), borderwidth=0)
        interior_id = self.canvas.create_window(0, 0, window=self.imageBox, anchor=NW)

        # track changes to the canvas and frame width and sync them, also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (self.imageBox.winfo_reqwidth(), self.imageBox.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if self.imageBox.winfo_reqwidth() != self.canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                self.canvas.config(width=self.imageBox.winfo_reqwidth())

        self.imageBox.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if self.imageBox.winfo_reqwidth() != self.imageBox.winfo_width():
                # update the inner frame's width to fill the canvas
                self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())

        self.canvas.bind('<Configure>', _configure_canvas)

    @staticmethod
    def id_to_image(id):
        return 'collectibles/collectibles_%s.png' % id.zfill(3)

    # image library stuff, from openbookproject.net
    def get_image(self, path):
        image = self._image_library.get(path)
        if image is None:
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            image = ImageTk.PhotoImage(Image.open(canonicalized_path))
            self._image_library[path] = image
        return image

    def updateWindow(self):
        # Make the height as large as it needs to be without resizing it if it's already large enough
        self.loadingMsg.grid(row=self.row, columnspan=5, sticky=EW)
        h = max(min(int(self.window.winfo_vrootheight() * 2 / 3), self.imageBox.winfo_height() + 4),
                self.window.winfo_height())
        self.window.geometry('%dx%d' % (self.imageBox.winfo_width() + self.scrollbar.winfo_width() + 2, h))
        self.window.update()

    def seedFindLabel(self, items):
        x = Label(self.imageBox, text='Desired Items:', foreground="#FFFFFF", background="#191919",
                  font=("Helvetica", 16))
        x.grid(row=self.row, column=0, columnspan=2, padx=0, pady=0, sticky=W)
        items += [None]*(3-len(items))
        for column, item in enumerate(items):
            if item:
                photo = self.get_image(self.id_to_image(str(item)))
            else:
                photo = self.get_image('collectibles/questionmark.png')
            x = Label(self.imageBox, image=photo, background="#191919")
            x.grid(row=self.row, column=column + 2, padx=0, pady=0, sticky=W)
        self.row += 1
        x = LabelFrame(self.imageBox)
        x.grid(row=self.row, columnspan=5, sticky=EW)
        self.row +=1
        self.updateWindow()

    def getSeedLabel(self):
        x = Label(self.imageBox, text='Seed', foreground="#FFFFFF", background="#191919", font=("Helvetica", 16))
        x.grid(row=self.row, column=0, padx=0, pady=0, sticky=W)
        self.row += 1
        self.updateWindow()

    def get_character_image(self, character):
        characters = ["The_Lost", "Eden", "Lazarus", "Azazel", "Samson", "Eve", "Blue_Baby", "Judas", "Cain",
                      "Magdalene", "Isaac"]
        return self.get_image('characters/' + characters[character] + '_App.png')

    def addSeed(self, number, character, items):
        try:
            # Use a text widget so the user can select and copy it
            x = Text(self.imageBox, width=len(str(number)), height=1, borderwidth=0, foreground="#FFFFFF",
                     background="#191919", font=("Helvetica", 16))
            x.insert(1.0, str(number))
            x.grid(row=self.row, column=0, padx=0, pady=0, sticky=W)
            x.configure(state="disabled")
            photo = self.get_character_image(character)
            x = Label(self.imageBox, image=photo, foreground="#FFFFFF", background="#191919", font=("Helvetica", 16))
            x.grid(row=self.row, column=1, padx=0, pady=0, sticky=W)
            for column, item in enumerate(items):
                photo = self.get_image(self.id_to_image(str(item)))
                x = Label(self.imageBox, image=photo, background="#191919")
                x.grid(row=self.row, column=column + 2, padx=0, pady=0, sticky=W)
            self.row += 1
            self.updateWindow()
        except:
            pass


def findSeeds():
    x = SeedsDisplay(iV)
    y = SeedFind(x)
    y.seedOut = x.addSeed
    mySeed = []
    character = findCharacter.current()
    for i in findItem:
        if i.get() != "Any":
            mySeed += [int(items[i.current()][0])]
    x.seedFindLabel(mySeed[:])
    x.updateWindow()
    y.findSeeds(mySeed, int(numSeeds.get()), int(offset.get()), character)
    try:
        x.updateWindow()
        x.loadingMsg.configure(text="Done!")
    except:
        pass


def showSeed():
    x = SeedsDisplay(iV)
    y = SeedFind(x)
    t = mySeed.get()
    theSeed = y.getSeed(t)
    x.getSeedLabel()
    for char, items in enumerate(theSeed):
        x.addSeed(t, char, items)
    try:
        x.updateWindow()
        x.loadingMsg.configure(text="Done!")
    except:
        pass


if __name__ == "__main__":
    with open("items.txt", "r") as f:
        items_info = json.load(f)
    items = items_info.items()
    items = [i for i in items if int(i[0]) in valid_items]
    items.sort(key=lambda w: w[1]['name'])

    iV = Tk()
    iV.wm_title("Diversity Mod Seed Finder")


    # **** Seed Finding GUI ****
    m = LabelFrame(iV, padx=5, pady=5)
    n = Label(m,
              text='Choose up to 3 items to search for seeds with characters starting those items.\n\nOffset indicates which seed # to start searching from so you\ncan search for the same items twice without finding repeat seeds',
              justify=CENTER)
    n.grid(row=0, column=0, columnspan=3)
    n = Frame(m)
    findCharacter = ttk.Combobox(n, state='readonly',
                                 values=["The Lost", "Eden", "Lazarus", "Azazel", "Samson", "Eve", "Blue Baby", "Judas",
                                         "Cain", "Magdalene", "Isaac", "Any Character"])
    findCharacter.current(11)
    findCharacter.pack()
    n.grid(row=1, column=0, columnspan=3)
    findItem = []
    n = Frame(m)
    findItem.append(ttk.Combobox(n, state='readonly', values=[item[1]['name'] for item in items] + ["Any"]))
    findItem[0].current(len(items))
    findItem[0].pack()
    n.grid(row=2, column=0)
    n = Frame(m)
    findItem.append(ttk.Combobox(n, state='readonly', values=[item[1]['name'] for item in items] + ["Any"]))
    findItem[1].current(len(items))
    findItem[1].pack()
    n.grid(row=2, column=1)
    n = Frame(m)
    findItem.append(ttk.Combobox(n, state='readonly', values=[item[1]['name'] for item in items] + ["Any"]))
    findItem[2].current(len(items))
    findItem[2].pack()
    n.grid(row=2, column=2)
    m.grid(pady=10, padx=10)

    # Number of seeds label/entry
    n = Label(m, text="# of seeds to find:")
    n.grid(row=3, column=0, sticky=W)

    numSeeds = StringVar()
    numberOfSeeds = Entry(m, width=4, textvariable=numSeeds)
    numberOfSeeds.insert(END, "10")

    def findSeeds_key(event):
        findSeeds()

    numberOfSeeds.bind("<Return>", findSeeds_key)
    numberOfSeeds.grid(row=3, column=0, sticky=E)


    # Seed offset label/entry
    n = Label(m, text="Offset:")
    n.grid(row=3, column=1, sticky=W)

    offset = StringVar()
    n = Entry(m, width=12, textvariable=offset)
    n.insert(END, "0")
    n.bind("<Return>", findSeeds_key)
    n.grid(row=3, column=1, sticky=E)

    n = Button(m, text="Find Seeds", command=findSeeds)
    n.grid(row=3, column=2)

    # **** Seed Listing GUI ****
    m = LabelFrame(iV, padx=5, pady=5)
    n = Label(m, justify=CENTER, text='Input a seed to display the characters and their respective items.')
    n.pack()
    mySeed = StringVar()
    seedText = Entry(m, justify=CENTER, font="font 32 bold", width=15, textvariable=mySeed)

    def seedText_key(event):
        showSeed()

    seedText.bind("<Return>", seedText_key)
    seedText.pack()
    n = Button(m, text="Show Seed", command=showSeed)
    n.pack()
    m.grid(pady=10)

    mainloop()
