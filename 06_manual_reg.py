"""
Manual target-based registration
"""
import copy
import open3d as o3d
from tools import las_to_o3d


def draw_registered_pcd(ref_point_cloud, oriented_point_cloud,transformation):
    ori_temp = copy.deepcopy(oriented_point_cloud)
    ref_temp = copy.deepcopy(ref_point_cloud)
    ori_temp.paint_uniform_color([1, 0, 0])
    ref_temp.paint_uniform_color([0, 1, 0])
    ori_temp.transform(transformation)
    o3d.visualization.draw_geometries([ori_temp, ref_temp])