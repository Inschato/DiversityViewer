__author__ = 'Inschato'
'''
Some Code borrowed from the Rebirth Item Tracker:
https://github.com/Hyphen-ated/RebirthItemTracker/

Borrowed code copyright (c) 2015, Brett824 and Hyphen-ated
All rights reserved.

New code copyright (c) 2016, Inschato

Images copyright (c) 2014, Nicalis, Inc.

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

from tkinter import *
from tkinter import filedialog as tkFileDialog
from tkinter import messagebox as tkMessageBox
import json
from os import sep
from random import shuffle, choice, seed, randint
from math import sqrt
from binascii import crc32
from PIL import Image, ImageTk
from string import ascii_uppercase, digits

debug = False
random_offset = False
valid_items = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
    11, 12, 13, 14, 17, 18, 19, 20, 21, 27,
    28, 32, 46, 48, 50, 51, 52, 53, 54, 55,
    57, 60, 62, 63, 64, 67, 68, 69, 70, 71,
    72, 73, 74, 75, 76, 79, 80, 81, 82, 87,
    88, 89, 90, 91, 94, 95, 96, 98, 99, 100,
    101, 103, 104, 106, 108, 109, 110, 112, 113, 114,
    115, 116, 117, 118, 120, 121, 122, 125, 128, 129,
    131, 132, 134, 138, 139, 140, 141, 142, 143, 144,
    148, 149, 150, 151, 152, 153, 154, 155, 156, 157,
    159, 161, 162, 163, 165, 167, 168, 169, 170, 172,
    173, 174, 178, 179, 180, 182, 183, 184, 185, 187,
    188, 189, 190, 191, 193, 195, 196, 197, 198, 199,
    200, 201, 202, 203, 204, 205, 206, 207, 208, 209,
    210, 211, 212, 213, 214, 215, 216, 217, 218, 219,
    220, 221, 222, 223, 224, 225, 227, 228, 229, 230,
    231, 232, 233, 234, 236, 237, 240, 241, 242, 243,
    244, 245, 246, 247, 248, 249, 250, 251, 252, 254,
    255, 256, 257, 259, 260, 261, 262, 264, 265, 266,
    267, 268, 269, 270, 271, 272, 273, 274, 275, 276,
    277, 278, 279, 280, 281, 299, 300, 301, 302, 303,
    304, 305, 306, 307, 308, 309, 310, 311, 312, 313,
    314, 315, 316, 317, 318, 319, 320, 321, 322, 327,
    328, 329, 330, 331, 332, 333, 335, 336, 337, 340,
    341, 342, 343, 345, 350, 353, 354, 356, 358, 359,
    360, 361, 362, 363, 364, 365, 366, 367, 368, 369,
    370, 371, 372, 373, 374, 375, 376, 377, 378, 379,
    380, 381, 384, 385, 387, 388, 389, 390, 391, 392,
    393, 394, 395, 397, 398, 399, 400, 401, 402, 403,
    404, 405, 407, 408, 409, 410, 411, 412, 413, 414,
    415, 416, 417, 418, 420, 423, 424, 425, 426, 429,
    430, 431, 432, 433, 435, 436, 438, 440
]


class SeedFind:
    """
    Class for finding seeds with specified items, or finding the items of a specific seed
    """

    def __init__(self, window):
        self.valid_items = valid_items
        self.window = window
        self.last_seed = 0
        with open("items.txt", "r") as f:
            self.items_info = json.load(f)

    def get_item_list(self, rng_seed):
        rng_seed = str(rng_seed)
        seed(crc32(bytes(rng_seed, 'UTF-8')))
        itemIDs = valid_items[:]
        shuffle(itemIDs)
        return itemIDs[0:3]

    def get_seed(self, desired_seed):
        return self.get_item_list(desired_seed)

    # Redefine me to redirect this output
    def seed_out(self, number, items):
        pass

    def find_seeds(self, desired_items, instances=1, offset=0):
        # Sanity check the input
        desired_items = frozenset(desired_items)
        fi = frozenset(filter_items)
        for ID in desired_items:
            if ID not in self.valid_items:
                print("Error, item(s) not in valid_items list.")
                self.window.window.destroy()
                return None
        if len(valid_items) - len(filter_items) < 3:
            tkMessageBox.showinfo("Sorry", "There are too many filtered items.")
            return None
        if len(desired_items) > 0 and not desired_items.isdisjoint(fi):
            tkMessageBox.showinfo("Sorry", "Whoops, one or more desired items in the filter list.")
            return None

        if instances == 0:
            return None

        # Initialize
        if type(offset) == int:
            next_seed = offset
        else:
            seed()
            rng_seed = randint(-10000000,10000000)
            next_seed = ''.join(choice(ascii_uppercase + digits) for _ in range(6))

        seeds_checked = 0
        seeds_found = 0
        result = []

        # Seed finding loop
        while True:
            # periodically refresh the window
            if not(seeds_checked % 512):
                try:
                    if not(seeds_checked % 4096):
                        self.window.loadingMsg.configure(text='Loading... (' + str(seeds_checked) + ' checked)')
                    self.window.update_window()
                except:
                    if debug==True:
                        import traceback
                        traceback.print_exc()
                    return None

            current_item_set = frozenset(self.get_item_list(next_seed))
            if (desired_items <= current_item_set) and fi.isdisjoint(current_item_set):
                result.append(next_seed)
                seeds_found += 1
                if not self.seed_out(next_seed, current_item_set) or seeds_found >= instances:
                    self.last_seed = next_seed
                    return result

            seeds_checked += 1
            if type(offset) == int:
                next_seed += 1
            else:
                seed(rng_seed + seeds_checked)
                next_seed = ''.join(choice(ascii_uppercase + digits) for _ in range(6))


class SeedsDisplay:
    """
    Class for displaying lists of seeds using character and item images
    """

    def __init__(self, parent=None, show_items=True):
        self.row = 0
        self.show_items=show_items
        self.rows = [] # for show_items
        self._image_library = {}
        with open("items.txt", "r") as f:
            self.items_info = json.load(f)
        self.valid_items = valid_items

        # Initialize the window
        self.window = Toplevel(parent) if parent else Tk()
        self.window.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        self.window.configure(background="#191919")
        self.window.title("Seed Viewer")
        self.window.resizable(0, 1)
        self.window.bind("<Home>", lambda event: self.canvas.yview_moveto(0))
        self.window.bind("<End>", lambda event: self.canvas.yview_moveto(1))
        self.window.bind("<Prior>", lambda event: self.canvas.yview_scroll(-1,'pages'))
        self.window.bind("<Next>", lambda event: self.canvas.yview_scroll(1,'pages'))
        self.window.tk.call('wm', 'iconphoto', self.window._w, ImageTk.PhotoImage(Image.open('collectibles/collectibles_091.png')))

        # Initialize the scrolling canvas
        self.canvas = Canvas(self.window, background="#191919", borderwidth=0)
        self.scrollbar = Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=200, height=200)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)

        # Scrolling code taken from:
        # http://stackoverflow.com/questions/16188420/python-tkinter-scrollbar-for-frame
        self.imageBox = LabelFrame(self.canvas, background="#191919", foreground="#800000", borderwidth=0)
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
        self.loadingMsg = Button(self.imageBox, text="Loading..", borderwidth=0, state='disabled')

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
            canonicalized_path = path.replace('/', sep).replace('\\', sep)
            image = ImageTk.PhotoImage(Image.open(canonicalized_path))
            self._image_library[path] = image
        return image

    def update_window(self):
        # Make the height as large as it needs to be without resizing it if it's already large enough
        self.loadingMsg.grid(row=self.row, columnspan=5, sticky=EW)
        self.window.update() # First, update the loading message size and new item (if applicable)
        height = max(min(int(self.window.winfo_vrootheight() * 2 / 3), self.imageBox.winfo_height() + 4),
                self.window.winfo_height())
        width = self.imageBox.winfo_width() + self.scrollbar.winfo_width() + 2
        self.window.geometry('%dx%d' % (width, height))
        self.window.update() # Then update with the newly calculated height

    def seed_find_label(self, items):
        widget = Label(self.imageBox, text='Desired Items:', foreground="#FFFFFF", background="#191919",
                  font=("Helvetica", 16))
        widget.grid(row=self.row, column=0, columnspan=2, padx=0, pady=0, sticky=W)
        items += [None] * (3 - len(items))
        for column, item in enumerate(items):
            if item:
                photo = self.get_image(self.id_to_image(str(item)))
            else:
                photo = self.get_image('collectibles/questionmark.png')
            widget = Label(self.imageBox, image=photo, background="#191919")
            widget.grid(row=self.row, column=column + 2, padx=0, pady=0, sticky=W)
        self.row += 1
        widget = LabelFrame(self.imageBox)
        widget.grid(row=self.row, columnspan=5, sticky=EW)
        self.row += 1
        self.update_window()

    def get_seed_label(self):
        widget = Label(self.imageBox, text='Seed', foreground="#FFFFFF", background="#191919", font=("Helvetica", 16))
        widget.grid(row=self.row, column=0, padx=0, pady=0, sticky=W)
        self.row += 1
        self.update_window()


    def add_seed(self, number, items):
        try:
            # Use a text widget so the user can select and copy it
            widget = Text(self.imageBox, width=len(str(number))+2, height=1, borderwidth=0, foreground="#FFFFFF",
                     background="#191919", font=("Helvetica", 16))
            widget.insert(1.0, str(number))
            widget.grid(row=self.row, column=0, padx=0, pady=0, sticky=W)
            widget.configure(state="disabled")
            def show_items(event, row):
                if event:
                    event.widget.destroy() # Remove the "Show Items" text
                for column, item in enumerate(items):
                    photo = self.get_image(self.id_to_image(str(item)))
                    widget = Label(self.imageBox, image=photo, background="#191919")
                    widget.grid(row=row, column=column + 2, padx=0, pady=0, sticky=W)
            if self.show_items == True:
                show_items(None, self.row)
            else:
                widget = Label(self.imageBox, text="Show Items", foreground="#FFFFFF", background="#191919", font=("Helvetica", 14))
                widget.row = self.row
                widget.bind("<Button-1>", lambda event: show_items(event, widget.row))
                widget.grid(row=self.row, column=2, columnspan=3, sticky=EW)
            self.row += 1
            self.update_window()
        except Exception as e:
            if str(e).startswith('bad window path name'):
                return False
            else:
                import traceback
                traceback.print_exc()
        return True




def find_seeds():
    display = SeedsDisplay(main_window, not filemenu.hide_items.get())
    seed_finder = SeedFind(display)
    seed_finder.seed_out = display.add_seed  # Redirect the output seeds to our display object as they are found.
    items_to_find = []
    for i in desired_items:
        if i.item != "Any":
            items_to_find += [int(i.item)]
    display.seed_find_label(items_to_find[:])
    display.update_window()
    try:
        number_of_seeds = int(numSeeds.get())
    except ValueError:
        number_of_seeds = 10
        numSeeds.set('10')
    try:
        seed()
        seed_offset = int(offset.get()) if not random_offset else 'Random'
    except ValueError:
        seed_offset = 0
        offset.set('0')
    if not seed_finder.find_seeds(items_to_find, number_of_seeds, seed_offset):
        try:
            display.window.destroy()
        except:
            pass
        display = None
        return
    try:
        def append_seed():
            display.loadingMsg.configure(state='disabled', text='Loading')
            if type(seed_finder.last_seed) == int:
                seed_finder.find_seeds(items_to_find, 1, seed_finder.last_seed+1)
            else:
                seed_finder.find_seeds(items_to_find, 1, 'Random')
            display.loadingMsg.configure(state='normal', text='Next Seed')
            display.canvas.yview_moveto(1)
        display.loadingMsg.destroy() # Remove the 'Loading...' text label
        display.loadingMsg = Button(display.imageBox, text="Next Seed", command=append_seed)
        normal_state = display.loadingMsg.configure('state')
        display.window.bind("<Return>", lambda event: append_seed() if display.loadingMsg.configure('state') == normal_state else None)
        display.update_window()
    except:
        if debug:
            import traceback
            traceback.print_exc()


def show_seeds():
    display = SeedsDisplay(main_window, not filemenu.hide_items.get())
    seed_finder = SeedFind(display)
    the_seed = seed_to_display.get().strip()
    seed_items = seed_finder.get_seed(the_seed)
    display.get_seed_label()
    display.add_seed(the_seed, seed_items)
    try:
        display.update_window()
        display.loadingMsg.configure(text="Done!")
    except:
        if debug:
            import traceback
            traceback.print_exc()

def toggle_random_offset():
    global random_offset
    random_offset = not random_offset
    if random_offset:
        offset_entry.delete(0, END)
        offset_entry.insert(END, "Random")
        offset_entry.configure(state="disabled")
    else:
        offset_entry.configure(state="normal")
        offset_entry.delete(0, END)
        offset_entry.insert(END, "0")

def update_filter_label():
    if len(filter_items) > 0:
        filter_label.configure(text="Filtering " + str(len(filter_items)) + " item" + ("s" if len(filter_items) > 1 else ""))
        filter_label.grid()
    else:
        filter_label.grid_remove()
    p = options.get('filter_dump_path')
    if p:
        items_list = []
        for item in filter_items:
            items_list.append(items_info[str(item).zfill(3)]['name'] + '\n')
        items_list.sort()
        try:
            with open(p, 'w') as f:
                f.writelines(items_list)
        except:
            pass

def filter_dump_set():
    f = tkFileDialog.asksaveasfilename(defaultextension='.txt')
    if f:
        options['filter_dump_path'] = f
        update_filter_label()

_image_library = {}
def id_to_image(i):
    if i == 'questionmark' or i == 'Any':
        return 'collectibles/questionmark.png'
    return 'collectibles/collectibles_%s.png' % i.zfill(3)

# image library stuff, from openbookproject.net
def get_image(path):
    image = _image_library.get(path)
    if image is None:
        canonicalized_path = path.replace('/', sep).replace('\\', sep)
        image = ImageTk.PhotoImage(Image.open(canonicalized_path))
        _image_library[path] = image
    return image

def filter_editor(parent):
    import re


    def filter_toggle(event):
        item = event.widget.item
        if item in filter_items:
            filter_items.remove(item)
            event.widget.configure(background="#191919")
        else:
            filter_items.append(item)
            event.widget.configure(background="#800000")
        update_filter_label()

    def filter_window_closed():
        global filter_window
        filter_window.destroy()
        filter_window = None

    def filter_all():
        global filter_items
        filter_items = valid_items[:]
        for widget in items_holder.winfo_children():
            widget.configure(background="#800000")
        update_filter_label()

    def filter_none():
        global filter_items
        filter_items = []
        for widget in items_holder.winfo_children():
            widget.configure(background="#191919")
        update_filter_label()

    def filter_search(sv):
        search_term = sv.get().lower()
        for widget in items_holder.winfo_children():
            item_name = items_info[str(widget.item).zfill(3)]['name'].lower()
            try:
                item_desc = items_info[str(widget.item).zfill(3)]['text'].lower()
            except:
                item_desc = ""
            try:
                if not re.search(search_term, item_name) and not re.search(search_term, item_desc):
                    widget.grid_remove()
                else:
                    widget.grid()
            except:
                widget.grid()

    def filter_search_toggle():
        for child in items_holder.winfo_children():
            if child.winfo_manager() != "":
                item_widget = child
                item = item_widget.item
                if item in filter_items:
                    filter_items.remove(item)
                    item_widget.configure(background="#191919")
                else:
                    filter_items.append(item)
                    item_widget.configure(background="#800000")
        update_filter_label()

    global filter_window
    if not filter_window:
        filter_window = Toplevel(parent)
        filter_window.iconify()
        filter_window.configure(background="#191919")
        filter_window.title("Filtered Items")
        filter_window.resizable(0, 0)
        filter_window.protocol("WM_DELETE_WINDOW", filter_window_closed)
        filter_window.tk.call('wm', 'iconphoto', filter_window._w, ImageTk.PhotoImage(Image.open('collectibles/collectibles_331.png')))
        widget_holder = Frame(filter_window, background="#191919")

        widget = Label(widget_holder, text="Click an item to add/remove it from the filter\n"+
                                           "Items in the filter will not appear as starting items in seeds",
                                           background="#191919", foreground="#FFFFFF")
        widget.grid(row=0, column=0,  padx=3)
        widget = Button(widget_holder, text="None", command=filter_none, background="#191919", foreground="#FFFFFF")
        widget.grid(row=0, column=1, padx=3)
        widget = Button(widget_holder, text="All", command=filter_all, padx=5, background="#191919", foreground="#FFFFFF")
        widget.grid(row=0, column=2, padx=3)
        widget = Label(widget_holder, text="Search:", background="#191919", foreground="#FFFFFF")
        widget.grid(row=0, column=3, padx=3)
        filter_search_string = StringVar()
        filter_search_string.trace("w", lambda name, index, mode, sv=filter_search_string: filter_search(sv))
        filter_search_entry = Entry(widget_holder, width=12, textvariable=filter_search_string)
        filter_search_entry.bind("<Escape>", lambda event: event.widget.delete(0,END))
        filter_search_entry.bind("<Return>", lambda event: filter_search_toggle())
        filter_search_entry.grid(row=0, column=4, sticky=E)
        widget_holder.grid()
        width = int(sqrt(len(items)))
        items_holder = Frame(filter_window, background="#191919")
        for index, item in enumerate(items):
            widget = Label(items_holder,  background=("#800000" if (int(item[0]) in filter_items) else "#191919"))
            widget.item = int(item[0])
            widget.img = get_image(id_to_image(str(item[0])))
            widget.configure(image=widget.img)
            widget.bind("<Button-1>", filter_toggle)
            widget.grid(row=int(index/width), column=index%width, padx=0, pady=0, sticky=W)
        items_holder.grid()
        items_holder.update()
        items_holder.grid_propagate(False)
        filter_search_entry.focus()
        filter_window.deiconify()
        filter_window.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))

# Where item_widget is the item label widget being selected for
def item_selector(parent, item_widget):
    global item_selector_window
    def destroy_window():
        global item_selector_window
        item_selector_window.destroy()
        item_selector_window = None

    def select_item(event):
        global item_selector_window
        item = event.widget.item
        item_selector_window.item_widget.item = item
        item_selector_window.item_widget.text.configure(text="Any Item" if item == 'Any' else items_info[str(item).zfill(3)]['name'])
        item_selector_window.item_widget.img = get_image(id_to_image(str(item)))
        item_selector_window.item_widget.configure(image=item_selector_window.item_widget.img)
        item_selector_window.destroy()
        item_selector_window = None

    def select_item_search():
        item = None
        for child in items_holder.winfo_children():
            if child.winfo_manager() != "" and item != None:
                return
            elif child.winfo_manager() != "":
                item = child.item
        if item:
            global item_selector_window
            item_selector_window.item_widget.item = item
            item_selector_window.item_widget.text.configure(text=items_info[str(item).zfill(3)]['name'])
            item_selector_window.item_widget.img = get_image(id_to_image(str(item)))
            item_selector_window.item_widget.configure(image=item_selector_window.item_widget.img)
            item_selector_window.destroy()
            item_selector_window = None

    def selector_search(sv):
        search_term = sv.get().lower()
        for widget in items_holder.winfo_children():
            if widget.item == 'Any':
                item_name = "."
            else:
                item_name = items_info[str(widget.item).zfill(3)]['name'].lower()
            try:
                item_desc = items_info[str(widget.item).zfill(3)]['text'].lower()
            except:
                item_desc = ""
            try:
                if widget.item in filter_items or (not re.search(search_term, item_name) and not re.search(search_term, item_desc)):
                    widget.grid_remove()
                else:
                    widget.grid()
            except:
                widget.grid()


    # If the window isn't open, or we're choosing for a different item
    if not item_selector_window or item_selector_window.item_widget != item_widget or item_selector_window.state() == 'iconic':
        if item_selector_window:
            item_selector_window.destroy()
        item_selector_window = Toplevel(parent)
        item_selector_window.iconify()
        item_selector_window.title("Select an Item")
        item_selector_window.resizable(False, False)
        item_selector_window.protocol("WM_DELETE_WINDOW", destroy_window)
        item_selector_window.tk.call('wm', 'iconphoto', item_selector_window._w, ImageTk.PhotoImage(Image.open('collectibles/questionmark.png')))
        item_selector_window.item_widget = item_widget


        width = int(sqrt(len(items)))
        widget_holder = Frame(item_selector_window)
        widget = Label(widget_holder, text="Search:")
        widget.grid(row=0, column=3, padx=3)
        selector_search_string = StringVar()
        selector_search_string.trace("w", lambda name, index, mode, sv=selector_search_string: selector_search(sv))
        widget = Entry(widget_holder, width=12, textvariable=selector_search_string)
        item_selector_window.search_entry = widget
        widget.bind("<Escape>", lambda event: event.widget.delete(0,END))
        widget.bind("<Return>", lambda event: select_item_search())
        widget.grid(row=0, column=4, sticky=E)
        widget_holder.grid()

        items_holder = Frame(item_selector_window)
        items_and_questionmark = items[:] + [['questionmark',None]]
        for index, item in enumerate(items_and_questionmark):
            widget = Label(items_holder)
            widget.item = int(item[0]) if item[0] != 'questionmark' else 'Any'
            widget.img = get_image(id_to_image(str(item[0])))
            widget.configure(image=widget.img)
            widget.bind("<Button-1>", select_item)
            widget.grid(row=int(index/width), column=index%width, padx=0, pady=0, sticky=W)
            if widget.item in filter_items:
                widget.grid_remove()
        items_holder.grid()
        items_holder.update()
        items_holder.grid_propagate(False)
        item_selector_window.search_entry.focus()
        item_selector_window.deiconify()
        item_selector_window.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))

def item_selector_reset(item_widget):
    item_widget.item = 'Any'
    item_widget.img = get_image(id_to_image('questionmark'))
    item_widget.text.configure(text="Any Item")
    item_widget.configure(image=item_widget.img)
    item_widget.update()


if __name__ == "__main__":

    with open("options.json", "r") as json_file:
        options = json.load(json_file)

    filter_items = options['filter_items']

    def save_options():
        options['hide_items'] = filemenu.hide_items.get()
        options['random_offset'] = filemenu.random_offset.get()
        options['filter_items'] = filter_items
        options['seeds'] = numSeeds.get()
        with open("options.json", "w") as json_file:
            json.dump(options, json_file, indent=3, sort_keys=True)
        main_window.destroy()

    with open("items.txt", "r") as f:
        items_info = json.load(f)
    items = items_info.items()
    items = [i for i in items if int(i[0]) in valid_items]
    items.sort(key=lambda w: w[1]['name'])
    items_info['Any'] = {'name':'Any Item', 'desc':''}
    filter_window = None
    item_selector_window = None

    main_window = Tk()
    main_window.wm_title("DM Viewer v0.5 for Diversity Mod v3.2.0")
    main_window.resizable(False,False)
    main_window.protocol("WM_DELETE_WINDOW", save_options)
    main_window.bind_class("Entry", "<Control-a>", lambda e: e.widget.selection_range(0,END))
    main_window.tk.call('wm', 'iconphoto', main_window._w, ImageTk.PhotoImage(Image.open('collectibles/collectibles_021.png')))

    # **** Seed Finding GUI ****
    widget_holder = LabelFrame(main_window, padx=5, pady=5)
    widget = Label(widget_holder,
                   text="Choose up to 3 items to search for seeds starting with those items.\n\n"
                   +"Offset indicates which seed # to start searching from so you\n"
                   +"can search for the same items twice without finding repeat seeds",
                   justify=CENTER)
    widget.grid(row=0, column=0, columnspan=3)
    widget = Frame(widget_holder)
    widget.grid(row=1, column=0, columnspan=3)

    desired_items = [None] * 3
    desired_items = [None]*3
    items_holder = LabelFrame(widget_holder)
    for index in range(0, len(desired_items)):
        widget = LabelFrame(items_holder)
        desired_items[index] = Label(widget)
        desired_items[index].text = Label(widget, text="Any Item")
        desired_items[index].img = get_image(id_to_image('questionmark'))
        desired_items[index].item = 'Any'
        desired_items[index].configure(image=desired_items[index].img)
        desired_items[index].bind("<Button 1>", lambda event: item_selector(main_window, event.widget))
        desired_items[index].bind("<Shift-Button 1>", lambda event: item_selector_reset(event.widget))

        desired_items[index].grid(row=0, column=index, pady=5)
        desired_items[index].text.grid(row=1, column=index, pady=2, padx=5)
        widget.grid(row=2, column=index)
    items_holder.grid(columnspan=3)
    widget_holder.grid(pady=10, padx=10)

    # Number of seeds label/entry/button
    widget = Label(widget_holder, text="# of seeds to find:")
    widget.grid(row=3, column=0, sticky=W)

    numSeeds = StringVar()
    widget = Entry(widget_holder, width=4, textvariable=numSeeds)
    widget.insert(END, str(options['seeds']))
    widget.bind("<Return>", lambda event: find_seeds())
    widget.grid(row=3, column=0, sticky=E)

    # Seed offset label/entry/button
    offset_label = Label(widget_holder, text="Offset:")
    offset_label.grid(row=3, column=1, sticky=W)

    offset = StringVar()
    offset_entry = Entry(widget_holder, width=12, textvariable=offset)
    offset_entry.insert(END, "0")
    offset_entry.bind("<Return>", lambda event: find_seeds())
    offset_entry.grid(row=3, column=1, sticky=E)
    if options['random_offset']:
        toggle_random_offset()

    widget = Button(widget_holder, text="Find Seeds", command=find_seeds)
    widget.grid(row=3, column=2)

    filter_label = Label(widget_holder, text="")
    filter_label.grid(row=1, column=2)
    filter_label.bind("<Button 1>", lambda event: filter_editor(main_window))
    update_filter_label()

    # **** Seed Displaying GUI ****
    widget_holder = LabelFrame(main_window, padx=5, pady=5)
    Label(widget_holder, justify=CENTER,
                   text='Input a seed to display the items on that seed.\n'\
                   +'Trailing spaces are ignored.').pack()

    seed_to_display = StringVar()
    widget = Entry(widget_holder, justify=CENTER, font="font 32 bold", width=15, textvariable=seed_to_display)
    widget.bind("<Return>", lambda event: show_seeds())
    widget.pack()

    Button(widget_holder, text="Show Seed", command=show_seeds).pack()
    widget_holder.grid(pady=10)


    # **** Menu Bar ****
    menu = Menu(main_window)
    main_window.config(menu=menu)
    filemenu = Menu(menu, tearoff=0)
    filemenu.hide_items = BooleanVar(value=options['hide_items'])
    filemenu.add_checkbutton(label="Hide Items", variable=filemenu.hide_items)
    filemenu.random_offset = BooleanVar(value=random_offset)
    filemenu.add_checkbutton(label="Random Seeds", command=toggle_random_offset, variable=filemenu.random_offset)
    filemenu.add_command(label="Edit Filter...", command=lambda : filter_editor(main_window))
    filemenu.add_command(label="Set Filter Dump Location...", command=lambda : filter_dump_set())
    menu.add_cascade(label="Settings", menu=filemenu)
    mainloop()
