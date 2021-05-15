"""------------------------------------------------------
Author: Mateusz Białek <mateusz.bialek.stud@pw.edu.pl>
Project for Computer Vision and 3D Data Processing course
MMNS, sem. 2, Warsaw University of Technology, 2021
------------------------------------------------------"""

import open3d as o3d
from tools import las_to_o3d

"""
Functions available in the visualizer:

-- Mouse view control --
Left button + drag : Rotate.
Ctrl + left button + drag : Translate.
Wheel button + drag : Translate.
Shift + left button + drag : Roll.
Wheel : Zoom in/out.
-- Keyboard view control --
[/] : Increase/decrease field of view.
R : Reset view point.
Ctrl/Cmd + C : Copy current view status into the clipboard.
Ctrl/Cmd + V : Paste view status from clipboard.
-- General control --
Q, Esc : Exit window.
H : Print help message.
P, PrtScn : Take a screen capture.
D : Take a depth capture.
O : Take a capture of current rendering settings.
"""


# Visualize point cloud
def show_pcd(point_clouds, window_name='Window name'):
    o3d.visualization.draw_geometries(point_clouds, window_name, width=1800, height=900, left=50, top=50)


# Visualize point cloud given file path
def visualize_cloud(path):
    lo3d = las_to_o3d(path)
    show_pcd([lo3d])


# Visualize two point clouds
def visualize_both(path1, path2):
    cloud1 = path1
    cloud2 = path2
    if isinstance(path1, str):
        cloud1 = las_to_o3d(path1)
    if isinstance(path2, str):
        cloud2 = las_to_o3d(path2)
    show_pcd([cloud1, cloud2], "Visualize both clouds")
