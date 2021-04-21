"""------------------------------------------------------
Author: Mateusz Białek <mateusz.bialek.stud@pw.edu.pl>
Project for Computer Vision and 3D Data Processing course
MMNS, sem. 2, Warsaw University of Technology, 2021
------------------------------------------------------"""
import open3d as o3d

from tools import read_point_cloud_o3d
import numpy as np


# Ball Pivoting surface reconstruction
def normals_estimation(point_cloud):
    print("Point cloud vertex normals estimation")
    point_cloud.normals = o3d.utility.Vector3dVector(np.zeros((1, 3)))  # If normals exist, then are removed
    return point_cloud.estimate_normals()


def ball_pivoting(point_cloud, ball_radius=(0.005, 0.01, 0.02, 0.04)):
    # point_cloud_normals = normals_estimation(point_cloud)
    print("Ball Pivoting surface reconstruction")
    tin = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(point_cloud,
                                                                          o3d.utility.DoubleVector(ball_radius))
    o3d.visualization.draw_geometries([point_cloud, tin])
    # o3d.visualization.draw_geometries([tin])


if __name__ == '__main__':
    pcd = read_point_cloud_o3d(
        "data/02_eagle/eagle.points.ply")
    ball_pivoting(pcd, ball_radius=[0.005, 0.01, 0.04])
    # ball_pivoting(pcd, ball_radius=[0.005, 0.01, 0.02, 0.04, 0.1, 0.2, 0.5, 0.9, 1.3])
