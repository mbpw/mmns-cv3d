# Import necessary libraries
import laspy
import numpy as np
import open3d as o3d


# Read point cloud with in-built I/O function
def read_point_cloud_o3d(filename):
    import open3d as o3d
    pcd = o3d.io.read_point_cloud(filename, format='auto', remove_nan_points=True, remove_infinite_points=True,
                                  print_progress=False)
    print(pcd)


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


lo3d = las_to_o3d('D:/! PW mgr/Sem2/[CV3D] Computer Vision and 3D data processing/proj/data/01_las/chmura_dj.las')
