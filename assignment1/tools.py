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


# Save LAS file with header generation
def save_points_with_header_generation(file, x, y, z, r, g, b, ext='pcd'):
    print('Header generation')
    header = laspy.header.Header(point_format=2)  # format=2 to add RGB
    las_pcd = laspy.file.File(file, header=header, mode="w")
    print('Compute max, min values')
    min_x = np.min(x)
    min_y = np.min(y)
    min_z = np.min(z)
    max_x = np.max(x)
    max_y = np.max(y)
    max_z = np.max(z)
    # mean_x = np.mean(x)
    # mean_y = np.mean(y)
    # mean_z = np.mean(z)
    # las_pcd.header.offset = [mean_x, mean_y, mean_z]
    las_pcd.header.offset = [0, 0, 0]
    las_pcd.header.max = [max_x, max_y, max_z]
    las_pcd.header.min = [min_x, min_y, min_z]
    # las_pcd.header.scale = [0.001, 0.001, 0.001]
    las_pcd.header.scale = [1.0, 1.0, 1.0]
    print("Saving cloud...")
    las_pcd.X = x
    las_pcd.Y = y
    las_pcd.Z = z
    if ext == 'pcd':
        r *= 255
        g *= 255
        b *= 255
    las_pcd.red = r
    las_pcd.green = g
    las_pcd.blue = b
    las_pcd.close()
    print("Point cloud successfuly saved!")


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


# Save LAS file with header copy
def save_pcd_as_las(file, pcd):
    """
    Save LAS file with header copy
    :param file:
    :param pcd:
    :return:
    """
    save_points_with_header_generation(file, *np.transpose(pcd.points), *np.transpose(pcd.colors))


def calculate_transformation_from_coords(refer, oriented):
    mean_s = np.mean(refer, 0)
    mean_t = np.mean(oriented, 0)

    # print(mean_s)
    # print(mean_t)

    ref_zeroed = refer - mean_s
    ori_zeroed = oriented - mean_t
    transposed = np.transpose(ori_zeroed)
    multiplcated = np.matmul(transposed, ref_zeroed)
    # print(multiplcated)

    S = np.eye(4, dtype=np.float64)
    U, D, VT = np.linalg.svd(multiplcated)
    # if np.linalg.det(U) * np.linalg.det(np.transpose(VT)) < 0:
    #     S[-1][-1] = -1
    # print(U)
    # print(D)
    # print(VT)
    # print(S)

    R = np.matmul(U, np.matmul(S, VT))
    # R = np.reshape(R, -1)
    R = np.transpose(R)
    t = np.reshape(mean_t, -1) - np.reshape(np.matmul(R, (np.transpose(mean_s))), -1)
    return R, t


if __name__ == '__main__':
    pcd = las_to_o3d("../data/01_las/chmura_dj.las")
    save_points_with_header_generation("result/test.las", *np.transpose(pcd.points), *np.transpose(pcd.colors))
    # print(np.transpose(pcd.points))
