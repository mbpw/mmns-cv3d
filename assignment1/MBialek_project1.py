"""------------------------------------------------------
Author: Mateusz Białek <mateusz.bialek.stud@pw.edu.pl>
Project for Computer Vision and 3D Data Processing course
MMNS, sem. 2, Warsaw University of Technology, 2021
------------------------------------------------------"""

from tkinter import *
from tkinter import filedialog
import threading

import visualization_module
import tools
from registration_module import *

# import numpy as np
# import open3d as o3d
#
# # Function available in the visualizer
# from tools import las_to_o3d

"""
Point clouds placeholders
"""
cloud1 = None
cloud2 = None

"""
GUI
"""
root = Tk()
root.title("")

e1 = Entry(root, width=50)
e1.grid(row=0, column=0)
# e1.insert(0, "FIRST POINT CLOUD")
e1.insert(0, "D:/PW_mgr/Sem2/[CV3D] Computer Vision and 3D data processing/proj/data/01_las/chmura_dj.las")

e2 = Entry(root, width=50)
e2.grid(row=1, column=0)
# e2.insert(0, "SECOND POINT CLOUD")
e2.insert(0,
          "D:/PW_mgr/Sem2/[CV3D] Computer Vision and 3D data processing/proj/data/01_las/chmura_zdjecia_naziemne.las")


def open_cloud_btn1():
    e1.delete(0, END)
    e1.insert(0, filedialog.askopenfilename())


def open_cloud_btn2():
    e2.delete(0, END)
    e2.insert(0, filedialog.askopenfilename())


b1 = Button(root, text="...", command=open_cloud_btn1)
b1.grid(row=0, column=1)

b2 = Button(root, text="...", command=open_cloud_btn2)
b2.grid(row=1, column=1)


def preview_1():
    visualization_module.visualize_cloud(e1.get())


def preview_2():
    visualization_module.visualize_cloud(e2.get())


b3 = Button(root, text="Preview", command=lambda: threading.Thread(target=preview_1).start())
b4 = Button(root, text="Preview", command=lambda: threading.Thread(target=preview_2).start())
b3.grid(row=0, column=2, padx=5)
b4.grid(row=1, column=2)

b7 = Button(root, text="Load",
            command=lambda: threading.Thread(target=load_cloud_memory, args=[e1.get(), 'c1']).start())
b8 = Button(root, text="Load",
            command=lambda: threading.Thread(target=load_cloud_memory, args=[e2.get(), 'c2']).start())
b7.grid(row=0, column=3, padx=5)
b8.grid(row=1, column=3)

b5 = Button(root, text="Visualize both", command=lambda: threading.Thread(target=visualize_both()).start())
b5.grid(row=0, column=4, rowspan=2)

debug_var = BooleanVar()


# Create popup
def show_popup(text):
    window = Toplevel()
    label = Label(window, text=f"You need to load {text} first!")
    label.pack(fill='x', padx=50, pady=5)
    button_close = Button(window, text="Close", command=window.destroy)
    button_close.pack(fill='x')
    return


def mtb_pick(method="Measurement", file=None):
    global cloud1, cloud2, debug_var
    if cloud1 is None or cloud2 is None:
        show_popup("both clouds")
        return
    debug = debug_var.get()
    _, oriented_c2 = manual_target_based(cloud1, cloud2, type=method, debug=debug, file=file)
    cloud2 = oriented_c2
    pass


def load_cloud_memory(path, c_number):
    global cloud1, cloud2
    temp_cloud = tools.las_to_o3d(path)
    if c_number == 'c1':
        cloud1 = temp_cloud
    elif c_number == 'c2':
        cloud2 = temp_cloud
    else:
        return
    print("Successfuly Loaded points from " + path + " to memory!")


def remove_noise(cloud):
    from outliers_module import outlier_remove_stats
    global cloud1, cloud2

    if cloud == 'c1':
        if cloud1 is None:
            show_popup("cloud 1")
            return
        print("Removing outliers for cloud 1...")
        filtered, deleted = outlier_remove_stats(cloud2, 30, 2.0)
        cloud1 = filtered
    elif cloud == 'c2':
        if cloud2 is None:
            show_popup("cloud 2")
            return
        print("Removing outliers for cloud 2...")
        filtered, deleted = outlier_remove_stats(cloud2, 30, 2.0)
        cloud2 = filtered


lbl1 = Label(root, text="Point clouds registration: ", anchor="e")
lbl1.grid(row=4, column=0)

chk1 = Checkbutton(root, variable=debug_var, onvalue=True, offvalue=False)

chk1.grid(row=4, column=1)

b6 = Button(root, text="Manual", command=lambda: threading.Thread(target=mtb_pick()).start())
b6.grid(row=4, column=2)

b9 = Button(root, text="From file", command=lambda: threading.Thread(target=mtb_pick("File", "File")).start())
b9.grid(row=4, column=3)

b10 = Button(root, text="DMatching", command=lambda: threading.Thread(target=mtb_pick("ICP")).start())
b10.grid(row=4, column=4, padx=5)

lbl2 = Label(root, text="Remove noise", anchor="e")
b11 = Button(root, text="Cloud 1", command=lambda: threading.Thread(target=remove_noise("c1")).start())
b12 = Button(root, text="Cloud 2", command=lambda: threading.Thread(target=remove_noise("c2")).start())
lbl2.grid(row=3, column=0)
b11.grid(row=3, column=2)
b12.grid(row=3, column=3)


def visualize_both():
    if cloud1 is None or cloud2 is None:
        visualization_module.visualize_both(e1.get(), e2.get())
    else:
        visualization_module.visualize_both(cloud1, cloud2)


# Start GUI loop
mainloop()
