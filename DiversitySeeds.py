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

    def get_item_list(self, rng_seed):
        seed(str(rng_seed))
        # creates list of 33 unique items from the valid items list
        return sample(self.valid_items, 33)

    def get_seed(self, desired_seed):
        chars = [None] * 11
        item_ids = self.get_item_list(desired_seed)
        for i in range(0, 11):
            chars[i] = item_ids[3 * i:(3 * i) + 3]
        return chars

    # Redefine me to redirect this output
    def seed_out(self, number, character, items):
        pass

    def find_seeds(self, desired_items, instances=1, offset=0, character=11):
        for ID in desired_items:
            if ID not in self.valid_items:
                print("Error, item(s) not in valid_items list.")
                self.window.window.destroy()
                return None
        next_seed = offset
        desired_items = frozenset(desired_items)
        seeds_found = 0
        result = []
        chars = [None] * 11
        while True:
            if next_seed % 1024:
                try:
                    self.window.window.update()
                except:
                    return
            item_ids = self.get_item_list(next_seed)
            if character == 11:
                for i in range(0, 11):
                    chars[i] = item_ids[3 * i:(3 * i) + 3]
            else:
                chars = [item_ids[3 * character:(3 * character) + 3]]
            for i, char in enumerate(chars):
                if not (desired_items <= set(char)):
                    continue
                result += [next_seed]
                seeds_found += 1
                self.seed_out(next_seed, i if character == 11 else character, char)
                if seeds_found >= instances:
                    return result
            next_seed += 1


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

        # Scrolling code taken from:
        # http://stackoverflow.com/questions/16188420/python-tkinter-scrollbar-for-frame
        self.imageBox = LabelFrame(self.canvas, background="#191919", foreground="#FF0000", borderwidth=0)
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
        self.loadingMsg = Label(self.imageBox, text="Loading..", background="#191919", foreground="#FFFFFF",
                                font=("Helvetica", 16), borderwidth=0)

        def _configure_canvas(event):
            if self.imageBox.winfo_reqwidth() != self.imageBox.winfo_width():
                # update the inner frame's width to fill the canvas
                self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())

        self.canvas.bind('<Configure>', _configure_canvas)

    @staticmethod
    def id_to_image(i):
        return 'collectibles/collectibles_%s.png' % i.zfill(3)

    # image library stuff, from openbookproject.net
    def get_image(self, path):
        image = self._image_library.get(path)
        if image is None:
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            image = ImageTk.PhotoImage(Image.open(canonicalized_path))
            self._image_library[path] = image
        return image

    def update_window(self):
        # Make the height as large as it needs to be without resizing it if it's already large enough
        self.loadingMsg.grid(row=self.row, columnspan=5, sticky=EW)
        h = max(min(int(self.window.winfo_vrootheight() * 2 / 3), self.imageBox.winfo_height() + 4),
                self.window.winfo_height())
        self.window.geometry('%dx%d' % (self.imageBox.winfo_width() + self.scrollbar.winfo_width() + 2, h))
        self.window.update()

    def seed_find_label(self, items):
        x = Label(self.imageBox, text='Desired Items:', foreground="#FFFFFF", background="#191919",
                  font=("Helvetica", 16))
        x.grid(row=self.row, column=0, columnspan=2, padx=0, pady=0, sticky=W)
        items += [None] * (3 - len(items))
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
        self.row += 1
        self.update_window()

    def get_seed_label(self):
        x = Label(self.imageBox, text='Seed', foreground="#FFFFFF", background="#191919", font=("Helvetica", 16))
        x.grid(row=self.row, column=0, padx=0, pady=0, sticky=W)
        self.row += 1
        self.update_window()

    def get_character_image(self, character):
        characters = ["The_Lost", "Eden", "Lazarus", "Azazel", "Samson", "Eve", "Blue_Baby", "Judas", "Cain",
                      "Magdalene", "Isaac"]
        return self.get_image('characters/' + characters[character] + '_App.png')

    def add_seed(self, number, character, items):
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
            self.update_window()
        except:
            pass


def find_seeds():
    display = SeedsDisplay(main_window)
    seed_finder = SeedFind(display)
    seed_finder.seed_out = display.add_seed  # Redirect the output seeds to our display object as they are found.
    character = selected_character.current()
    items_to_find = []
    for i in desired_items:
        if i.get() != "Any":
            items_to_find += [int(items[i.current()][0])]
    display.seed_find_label(items_to_find[:])
    display.update_window()
    seed_finder.find_seeds(items_to_find, int(numSeeds.get()), int(offset.get()), character)
    try:
        display.update_window()
        display.loadingMsg.configure(text="Done!")
    except:
        pass


def show_seeds():
    display = SeedsDisplay(main_window)
    seed_finder = SeedFind(display)
    the_seed = seed_to_display.get().strip()
    seed_items = seed_finder.get_seed(the_seed)
    display.get_seed_label()
    for char, items in enumerate(seed_items):
        display.add_seed(the_seed, char, items)
    try:
        display.update_window()
        display.loadingMsg.configure(text="Done!")
    except:
        pass


if __name__ == "__main__":
    with open("items.txt", "r") as f:
        items_info = json.load(f)
    items = items_info.items()
    items = [i for i in items if int(i[0]) in valid_items]
    items.sort(key=lambda w: w[1]['name'])

    main_window = Tk()
    main_window.wm_title("Diversity Mod Seed Finder")

    # **** Seed Finding GUI ****
    widget_holder = LabelFrame(main_window, padx=5, pady=5)
    widget = Label(widget_holder,
                   text='Choose up to 3 items to search for seeds with characters starting those items.\n\n\
                   Offset indicates which seed # to start searching from so you\n\
                   can search for the same items twice without finding repeat seeds',
                   justify=CENTER)
    widget.grid(row=0, column=0, columnspan=3)
    widget = Frame(widget_holder)
    selected_character = ttk.Combobox(widget, state='readonly',
                                      values=["The Lost", "Eden", "Lazarus", "Azazel", "Samson", "Eve", "Blue Baby",
                                              "Judas",
                                              "Cain", "Magdalene", "Isaac", "Any Character"])
    selected_character.current(11)
    selected_character.pack()
    widget.grid(row=1, column=0, columnspan=3)
    desired_items = [None] * 3
    for index in range(0, len(desired_items)):
        widget = Frame(widget_holder)
        desired_items[index] = ttk.Combobox(widget, state='readonly',
                                            values=[item[1]['name'] for item in items] + ["Any"])
        desired_items[index].current(len(items))
        desired_items[index].pack()
        widget.grid(row=2, column=index)
    widget_holder.grid(pady=10, padx=10)

    # Number of seeds label/entry/button
    widget = Label(widget_holder, text="# of seeds to find:")
    widget.grid(row=3, column=0, sticky=W)

    numSeeds = StringVar()
    widget = Entry(widget_holder, width=4, textvariable=numSeeds)
    widget.insert(END, "10")
    widget.bind("<Return>", lambda event: find_seeds())
    widget.grid(row=3, column=0, sticky=E)

    # Seed offset label/entry/button
    widget = Label(widget_holder, text="Offset:")
    widget.grid(row=3, column=1, sticky=W)

    offset = StringVar()
    widget = Entry(widget_holder, width=12, textvariable=offset)
    widget.insert(END, "0")
    widget.bind("<Return>", lambda event: find_seeds())
    widget.grid(row=3, column=1, sticky=E)

    widget = Button(widget_holder, text="Find Seeds", command=find_seeds)
    widget.grid(row=3, column=2)

    # **** Seed Displaying GUI ****
    widget_holder = LabelFrame(main_window, padx=5, pady=5)
    widget = Label(widget_holder, justify=CENTER,
                   text='Input a seed to display the characters and their respective items.\n\
                   Trailing spaces are ignored.')
    widget.pack()

    seed_to_display = StringVar()
    widget = Entry(widget_holder, justify=CENTER, font="font 32 bold", width=15, textvariable=seed_to_display)
    widget.bind("<Return>", lambda event: show_seeds())
    widget.pack()

    widget = Button(widget_holder, text="Show Seed", command=show_seeds)
    widget.pack()
    widget_holder.grid(pady=10)

    mainloop()
