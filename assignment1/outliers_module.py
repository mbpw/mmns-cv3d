"""------------------------------------------------------
Author: Mateusz Białek <mateusz.bialek.stud@pw.edu.pl>
Project for Computer Vision and 3D Data Processing course
MMNS, sem. 2, Warsaw University of Technology, 2021
------------------------------------------------------"""
import open3d as o3d


def outlier_remove_stats(point_cloud, n_neighbour=30, std_ratio=2.0):
    """
    Point cloud filtering using StatisticalOutlierRemoval method
    :param point_cloud:
    :param n_neighbour:
    :param std_ratio:
    :return:
    """
    filtered_point_cloud, ind = point_cloud.remove_statistical_outlier(nb_neighbors=n_neighbour, std_ratio=std_ratio)
    outliers = point_cloud.select_by_index(ind, invert=True)
    print("Draw point clouds - outliers (red colour), point_cloud (RGB) ")
    outliers.paint_uniform_color([1, 0, 0])
    o3d.visualization.draw_geometries([filtered_point_cloud, outliers])
    return filtered_point_cloud, outliers


def outlier_remove_sphere(point_cloud, nb_pts=30, r=1.0):
    """
    Point cloud filtering using r-meter radius sphere
    :param point_cloud:
    :param nb_pts:
    :param r:
    :return:
    """
    filtered_point_cloud, ind = point_cloud.remove_radius_outlier(nb_points=nb_pts, radius=r)
    outliers = point_cloud.select_by_index(ind, invert=True)
    print("Draw point clouds - outliers (red colour), point_cloud (RGB): ")
    outliers.paint_uniform_color([1, 0, 0])
    o3d.visualization.draw_geometries([filtered_point_cloud, outliers])
    return filtered_point_cloud, outliers
