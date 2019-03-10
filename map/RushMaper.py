import tkinter as tk
import json
from tkinter import simpledialog, filedialog, ttk, messagebox
import tools
from pathlib import Path


import map_editor as me


VERSION = (0,0,1)

root = tk.Tk()

def initiate_file():
    filename = ''
    while filename == '':
        filename = str(simpledialog.askstring('New Map', 'Enter your map name')).strip()
        if filename == None:
            return None
        if Path(filename + '.json').is_file():
            messagebox.showerror('Error', '\'{}\' already existed!'.format(filename + '.rm.json'))
            filename = ''

    imagename = None
    while not imagename:
        messagebox.showinfo('Done', 'Next, please select map image file')
        imagename = filedialog.askopenfilename(filetypes=(("GIF Image", "*.gif"),
                                                ("PGM Image", "*.pgm"),
                                                ("PPM Image", "*.ppm") ))

    with open(filename + '.rd.json', 'w') as fd:
        data = {}
        nodes = {}
        data['nodes'] = nodes
        data['version'] = VERSION

        json.dump(data, fd)

    with open(filename + '.rm.json', 'w') as f:
        data = {}
        nodes = {}
        links = []

        data['version'] = VERSION
        data['imagename'] = imagename

        data['nodes'] = nodes
        data['links'] = links

        json.dump(data, f)

        return f


def click_open():
    path = None
    if path == None:
        path = filedialog.askopenfilename()

    print('AAAAAAA')
    print(path)
    # f = tools.get_file(path)
    f = open(path, 'r')

    root.destroy()
    me.start(f)

def click_new():
    f = initiate_file()
    root.destroy()
    me.start(f)


tk.Label(root, text='RushMaper').pack()
ttk.Button(root, text='New', command=click_new).pack()
ttk.Button(root, text='Open', command=click_open).pack()

root.mainloop()




# root.update()
# f = filedialog.askopenfile()
# print(f.read())

# map_img = tk.PhotoImage(file='sample.gif')



# map_bg = tk.Label(root, image = map_img)
# map_bg.pack()

# button_save = tk.Button(root, text='Save', command=save, fg='red')
# button_save.pack()

# root.bind('<Motion>', cursor_move)
# root.bind("<Button 1>", cursor_click)
# root.mainloop()