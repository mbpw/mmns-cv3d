"""------------------------------------------------------
Author: Mateusz Białek <mateusz.bialek.stud@pw.edu.pl>
Project for Computer Vision and 3D Data Processing course
MMNS, sem. 2, Warsaw University of Technology, 2021
------------------------------------------------------"""
# Visulization of point cloud using Open3D
import copy

import numpy as np
import open3d as o3d

# Function available in the visualizer
from tools import las_to_o3d

"""
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
    o3d.visualization.draw_geometries(point_clouds, window_name, width=1920, height=1080, left=50, top=50)


def visualize_cloud(path):
    lo3d = las_to_o3d(path)
    show_pcd([lo3d])


def visualize_both(path1, path2):
    if isinstance(path1, str) and isinstance(path2, str):
        cloud1 = las_to_o3d(path1)
        cloud2 = las_to_o3d(path2)
    else:
        cloud1 = path1
        cloud2 = path2
    transformation = np.identity(4)

    # ori_temp = copy.deepcopy(cloud1)
    # ref_temp = copy.deepcopy(cloud2)
    # ori_temp.paint_uniform_color([1, 0, 0])
    # ref_temp.paint_uniform_color([0, 1, 0])
    # ori_temp.transform(transformation)

    # o3d.visualization.draw_geometries([ori_temp, ref_temp], "window_name", width=1920, height=1080, left=50, top=50)
    show_pcd([cloud1, cloud2])
