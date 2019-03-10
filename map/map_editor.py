import tkinter as tk
import json
from tkinter import simpledialog, filedialog, ttk, Canvas, messagebox, Scrollbar, Listbox
import tools

data = {}
filename = None
image = None
root = None
sub = None
canvas = None
editing = False
mode = 0
nodes_text = []
nodes_circle = []

linking = []
linking_c = []

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

def click_node(event, key):

    global data, editing, mode, linking, linking_c, canvas

    

    print(key)

    if mode == 1:

        def on_confirm():
            name = str(e1.get()).strip()
            if name != '':
                coo = data['nodes'][key]
                data['nodes'].pop(key, None)
                data['nodes'][name] = coo

            update_nodes()
            edit.destroy()

        def on_delete():
            data['nodes'].pop(key, None)

            update_nodes()
            edit.destroy()
        
        def on_cancel():
            edit.destroy()

        edit = tk.Tk()

        tk.Label(edit, text="Name").grid(row=0)
        tk.Label(edit, text="(X,Y)").grid(row=1)

        e1 = tk.Entry(edit)
        e1.insert(10, key)
        # e2 = tk.Entry(edit)

        e1.grid(row=0, column=1)
        # e2.grid(row=1, column=1)

        tk.Button(edit, text='Comfirm', command=on_confirm).grid(row=3, column=0)
        tk.Button(edit, text='Delete This Node', command=on_delete).grid(row=3, column=1)
        tk.Button(edit, text='Cancle', command=on_cancel).grid(row=3, column=2)

        edit.mainloop()
    if mode == 2 or mode == 3:
        if len(linking) < 1:
            linking.append(key)
            c = canvas.find_withtag('c:' + key)
            canvas.itemconfig(c, fill='red')
            linking_c.append(c)
        else:
            def is_repeat(linkt):
                for i, l in enumerate(data['links']):
                    if link[0] == l[0] and link[1] == l[1]:
                        return i

                return False

            if key != linking[0]:
                linking.append(key)
                # linking_c.append(c)

                # print(linking_c)

                linking = sorted(linking)
                link = (linking[0], linking[1])

                i = is_repeat(link)

                if not i:
                    data['links'].append(link)
                else:
                    data['links'].pop(i)
                # print(linking)

            for c in linking_c:
                canvas.itemconfig(c, fill='gray')

            linking.clear()
            linking_c.clear()

            update_nodes()

def data_editor():

    def init_data():
        with open(filename + '.rd.json', 'r') as f:
            imported = json.load(f)
            data_dict['version'] = imported['version']
            for key in data['nodes']:
                if key in imported['nodes']:
                    data_dict['nodes'][key] = imported['nodes'][key]
                else:
                    data_dict['nodes'][key] = 'Unnamed'

    def select(event):
        print(mylist.selection_get())
        key = str(mylist.selection_get()).split(':')[0]
        string = simpledialog.askstring('Edit name', 'Enter name for node : ' + key)
        if string and string != '':
            data_dict['nodes'][key] = string
        with open(filename + '.rd.json', 'w') as f:
            json.dump(data_dict, f)
            print('Dumped to : ' + f.name)
        insert_data()

    def insert_data():
        mylist.delete(0, tk.END)
        for key in data_dict['nodes']:
            mylist.insert(tk.END, key + ':' + data_dict['nodes'][key])

    data_dict = {}
    data_nodes_dict = {}
    data_dict['nodes'] = data_nodes_dict

    data_editing = False

    init_data()

    data_f = tk.Tk()
    scrollbar = Scrollbar(data_f)
    scrollbar.pack( side = tk.RIGHT, fill = tk.Y )

    mylist = Listbox(data_f, yscrollcommand = scrollbar.set )
    insert_data()

    mylist.pack( side = tk.LEFT, fill = tk.BOTH )
    scrollbar.config( command = mylist.yview )

    mylist.bind('<Double-1>', select)

    data_f.mainloop()


def update_nodes():


    global data, root, sub, canvas, nodes_text, nodes_circle

    print(data)

    for nt in nodes_text:
        nt.pack_forget()

    nodes_text.clear()
    canvas.delete("all")
    canvas.create_image(image.width()/2, image.height()/2, image = image)

    for key in data['nodes']:
        x, y = data['nodes'][key][0], data['nodes'][key][1]

        print(';;;;TEXTTTT;;;')
        print(key)
        print(str(data['nodes'][key]))
        text = '{} : {}'.format(str(key), str(data['nodes'][key]))
        t = tk.Label(sub, text=text)
        t.pack()
        nodes_text.append(t)

        cc = canvas.create_circle(x, y, 10, fill='gray', tags='c:' + key)
        ct = canvas.create_text(x, y, text=key, state=tk.DISABLED)

        canvas.tag_bind(cc, '<Button-1>', lambda event, key=key: click_node(event, key))
        # canvas.tag_bind(ct, '<Button-1>', lambda event, key=key: click_node(event, key))
        # c.pack()
        # nodes_circle.append(c)
    for link in data['links']:
        key1, key2 = link[0], link[1]
        x1, y1 = data['nodes'][key1][0], data['nodes'][key1][1]
        x2, y2 = data['nodes'][key2][0], data['nodes'][key2][1]

        canvas.create_line(x1, y1, x2, y2, fill='blue', state=tk.DISABLED)
    # sub.mainloop()


def cursor_move(event):
        pass
        # print(str(x) + ', ' + str(y))

def cursor_click(event):

    global data, editing

    print(str(event.widget)[0:8])
    if str(event.widget)[0:8] != '.!button' and mode == 0:
        x, y = event.x, event.y
        if x >= 0 and y >= 0 and x <= image.width() and y <= image.height():
            node_name = simpledialog.askstring("New Node", "Enter node's name\n{}, {}".format(x, y))
            if str(node_name).strip() != '' and node_name != None:
                print(node_name)
                coo = (x, y)
                print(coo)

                data['nodes'][node_name] = coo

                update_nodes()
    # else:
    #     root.destroy()

def save(event=None):
    global filename
    with open(filename + '.rm.json', 'w') as f:
        json.dump(data, f)
        f.close()

    messagebox.showinfo('Done', 'It passed the progress that it saved, but I don\'t know if it success or not!')
    

def initial_data(file):
    global data, image, filename

    filename = (str(file.name).split('.'))[0]
    file.close()

    with open(filename + '.rm.json', 'r') as f:
        data = json.load(f)
        f.close()

    image_filename = data['imagename']
    image = tk.PhotoImage(file=image_filename)

    print(image_filename)
    

def quitall():
    global root, sub
    root.destroy()
    sub.destroy()
    exit()

def start(file):

    def edit():
        global mode
        mode = (mode + 1) % 3

        if mode == 0: button_edit_text.set('Add Mode')
        if mode == 1: button_edit_text.set('Edit Mode')
        if mode == 2: button_edit_text.set('Link Mode')
        if mode == 3: button_edit_text.set('Delete Link Mode')

    global root, sub, canvas, image, filename
    root = tk.Tk()
    sub = tk.Tk()
    root.title('Datas')
    sub.title('Nodes')
    

    initial_data(file)

    print(image.width())
    print(image.height())


    canvas = tk.Canvas(root, width = image.width(), height = image.height(), bg = 'white')
    

    update_nodes()
    canvas.pack()
    # map_bg = tk.Label(root, image = image)
    # map_bg.pack()

    button_save = ttk.Button(root, text='Save', command=save)
    button_save.pack()

    button_edit_text = tk.StringVar()
    button_edit = ttk.Button(root, textvariable=button_edit_text, command=edit)
    button_edit_text.set('Add Mode')
    button_edit.pack()

    ttk.Button(root, text='Data Editor', command=data_editor).pack()

    ttk.Button(root, text='Quit', command=quitall).pack()

    root.bind('<Motion>', cursor_move)
    root.bind("<Button 1>", cursor_click)
    # tk.Label(sub, text='None').pack()
    root.mainloop()
    sub.mainloop()


if __name__ == '__main__':
    start(open('ser.rm.json', 'r'))