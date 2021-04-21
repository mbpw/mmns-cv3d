"""------------------------------------------------------
Author: Mateusz Białek <mateusz.bialek.stud@pw.edu.pl>
Project for Computer Vision and 3D Data Processing course
MMNS, sem. 2, Warsaw University of Technology, 2021
------------------------------------------------------"""
import copy
import laspy
import numpy as np
import open3d as o3d


# Read point cloud with in-built I/O function
def read_point_cloud_o3d(filename):
    pcd = o3d.io.read_point_cloud(filename, format='auto', remove_nan_points=True, remove_infinite_points=True,
                                  print_progress=False)
    return pcd


# Import LAS file
def las_to_o3d(file):
    las_pcd = laspy.file.File(file, mode='r')
    x = las_pcd.x
    y = las_pcd.y
    z = las_pcd.z
    # Colour normalization
    r = las_pcd.red / max(las_pcd.red)
    g = las_pcd.green / max(las_pcd.green)
    b = las_pcd.blue / max(las_pcd.blue)
    # Form NumPy to o3d
    las_points = np.vstack((x, y, z)).transpose()
    las_colors = np.vstack((r, g, b)).transpose()
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(las_points)
    point_cloud.colors = o3d.utility.Vector3dVector(las_colors)
    return point_cloud


# Manual point picking
def manual_point_picking(point_cloud):
    print("Manual point measurement")
    print("The data processing steps:")
    print(" (1.1) Point measurement - shift + left mouse button")
    print(" (1.2) The undo point picking - shift + right mouse button")
    print(" (2) End of measurement - press Q button")
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window(window_name='Manual point picking')
    vis.add_geometry(point_cloud)
    vis.run()  # user picks points
    vis.destroy_window()
    print("The end of measurement")
    print(vis.get_picked_points())
    return vis.get_picked_points()


def draw_registered_pcd(ref_point_cloud, oriented_point_cloud, transformation):
    ori_temp = copy.deepcopy(oriented_point_cloud)
    ref_temp = copy.deepcopy(ref_point_cloud)
    ori_temp.paint_uniform_color([1, 0, 0])
    ref_temp.paint_uniform_color([0, 1, 0])
    ori_temp.transform(transformation)
    o3d.visualization.draw_geometries([ori_temp, ref_temp])
