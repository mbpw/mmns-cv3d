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
from mesh_module import poisson_filtration

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

debug_var = BooleanVar()

e1 = Entry(root, width=80)
e1.grid(row=0, column=0)
e1.insert(0, "D:/PW_mgr/Sem2/[CV3D] Computer Vision and 3D data processing/proj/data/01_las/chmura_dj.las")

e2 = Entry(root, width=80)
e2.grid(row=1, column=0)
e2.insert(0,
          "D:/PW_mgr/Sem2/[CV3D] Computer Vision and 3D data processing/proj/data/01_las/chmura_zdjecia_naziemne.las")

b1 = Button(root, text="...", command=lambda: open_cloud_btn1())
b1.grid(row=0, column=1)

b2 = Button(root, text="...", command=lambda: open_cloud_btn2())
b2.grid(row=1, column=1)

b3 = Button(root, text="Preview", command=lambda: threading.Thread(target=preview('c1')).start())
b4 = Button(root, text="Preview", command=lambda: threading.Thread(target=preview('c2')).start())
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

"""BASIC GUI AND PCD VISUALIZATION FUNCTIONS"""


def open_cloud_btn1():
    e1.delete(0, END)
    e1.insert(0, filedialog.askopenfilename(filetypes=[("LAS point cloud", ".las")]))


def open_cloud_btn2():
    e2.delete(0, END)
    e2.insert(0, filedialog.askopenfilename())


def show_popup(text):
    """
    Create popup forcing user to load cloud(s) first

    :param text: text to display
    :type text: str
    :return: -
    """
    window = Toplevel()
    label = Label(window, text=f"You need to load {text} first!")
    label.pack(fill='x', padx=50, pady=5)
    button_close = Button(window, text="Close", command=window.destroy)
    button_close.pack(fill='x')
    return


def preview(cloud_no):
    if cloud_no == 'c1':
        visualization_module.visualize_cloud(e1.get())
    if cloud_no == 'c2':
        visualization_module.visualize_cloud(e2.get())


def visualize_both():
    if cloud1 is None or cloud2 is None:
        if cloud1 is not None:
            visualization_module.visualize_both(cloud1, e2.get())
        elif cloud2 is not None:
            visualization_module.visualize_both(e1.get(), cloud2)
        else:
            visualization_module.visualize_both(e1.get(), e2.get())
    else:
        visualization_module.visualize_both(cloud1, cloud2)


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


"""
DOWNSAMPLING
"""


def downsample(cloud):
    # TODO: parameters
    from downsampling_module import voxel_downsampling
    global cloud1, cloud2

    if cloud == 'c1':
        if cloud1 is None:
            show_popup("cloud 1")
            return
        print("Downsampling cloud 1...")
        downsampled = voxel_downsampling(cloud1, 0.1)
        cloud1 = downsampled
    elif cloud == 'c2':
        if cloud2 is None:
            show_popup("cloud 2")
            return
        print("Downsampling cloud 2...")
        downsampled = voxel_downsampling(cloud2, 0.1)
        cloud2 = downsampled


lbl3 = Label(root, text="Downsample:", anchor="e")
b13 = Button(root, text="Cloud 1", command=lambda: threading.Thread(target=downsample("c1")).start())
b14 = Button(root, text="Cloud 2", command=lambda: threading.Thread(target=downsample("c2")).start())
lbl3.grid(row=3, column=0, sticky='e')
b13.grid(row=3, column=2)
b14.grid(row=3, column=3)

"""
OUTLIERS
"""


def remove_noise(cloud):
    # TODO: parameters
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


lbl2 = Label(root, text="Remove noise:", anchor="e")
b11 = Button(root, text="Cloud 1", command=lambda: threading.Thread(target=remove_noise("c1")).start())
b12 = Button(root, text="Cloud 2", command=lambda: threading.Thread(target=remove_noise("c2")).start())
lbl2.grid(row=4, column=0, sticky='e')
b11.grid(row=4, column=2)
b12.grid(row=4, column=3)

"""
REGISTRATION
"""


def registration(algorithm="tb", method="Measurement", file=None):
    global cloud1, cloud2, debug_var
    if cloud1 is None or cloud2 is None:
        show_popup("both clouds")
        return
    debug = debug_var.get()
    if algorithm == 'tb' or algorithm == 'TB':
        _, oriented_c2 = registration_target_based(cloud1, cloud2, type=method, debug=debug, file=file)
        cloud2 = oriented_c2
    elif algorithm == 'icp' or algorithm == 'ICP':
        if method == '' or method == 'Measurement':
            method = 'p2p'
        trans, info = registration_ICP(cloud1, cloud2, method=method)
        print(info)
        cloud2.transform(trans)
    pass


lbl1 = Label(root, text="Point clouds target-based registration:", anchor="e")
lbl1.grid(row=5, column=0, sticky='e')

chk1 = Checkbutton(root, variable=debug_var, onvalue=True, offvalue=False)

chk1.grid(row=5, column=1)

b6 = Button(root, text="Manual", command=lambda: threading.Thread(target=registration("TB", "Measurement")).start())
b6.grid(row=5, column=2)

b9 = Button(root, text="From file", command=lambda: threading.Thread(target=registration("TB", "File", "File")).start())
b9.grid(row=5, column=3)

b10 = Button(root, text="DMatching", command=lambda: threading.Thread(target=registration("TB", "DM")).start())
b10.grid(row=5, column=4, padx=5)

lbl3 = Label(root, text="Point clouds ICP registration:", anchor="e")
lbl3.grid(row=6, column=0, sticky='e')
b15 = Button(root, text="Point2Point", command=lambda: threading.Thread(target=registration("ICP", "p2p")).start())
b15.grid(row=6, column=2)

b16 = Button(root, text="Point2Plane", command=lambda: threading.Thread(target=registration("ICP", "p2pl")).start())
b16.grid(row=6, column=3)

b17 = Button(root, text="ColoredICP", command=lambda: threading.Thread(target=registration("ICP", "cicp")).start())
b17.grid(row=6, column=4, padx=5)

"""
COMBINE CLOUDS AND CREATE TIN
"""


def generate_mesh():
    if cloud1 is None or cloud2 is None:
        show_popup("both clouds")
        return
    file = filedialog.asksaveasfilename()
    if file is not None:
        print("Combining two point clouds...")
        combined = cloud1 + cloud2
        print("Saving...")
        poisson_filtration(combined, file, True)


b15 = Button(root, text="Generate Mesh", command=lambda: threading.Thread(target=generate_mesh()).start)
b15.grid(row=7, column=0)

# Start GUI loop
mainloop()
