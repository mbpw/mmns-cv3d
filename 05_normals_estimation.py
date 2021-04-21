"""------------------------------------------------------
Author: Mateusz Białek <mateusz.bialek.stud@pw.edu.pl>
Project for Computer Vision and 3D Data Processing course
MMNS, sem. 2, Warsaw University of Technology, 2021
------------------------------------------------------"""
from tools import read_point_cloud_o3d
import open3d as o3d

pcd = read_point_cloud_o3d(
    "data/02_eagle/eagle.points.ply")

pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
