import open3d as o3d

from tools import las_to_o3d


# Filtracja chmur punktów metodą StatisticalOutlierRemoval
def outlier_remove(point_cloud, n_neighbour=30, std_ratio=2.0):
    filtered_point_cloud, ind = point_cloud.remove_statistical_outlier(nb_neighbors=n_neighbour, std_ratio=std_ratio)
    outliers = point_cloud.select_by_index(ind, invert=True)
    print("Draw point clouds - outliers (red colour), point_cloud (RGB) ")
    outliers.paint_uniform_color([1, 0, 0])
    o3d.visualization.draw_geometries([filtered_point_cloud, outliers])
    return filtered_point_cloud, outliers


lo3d = las_to_o3d('D:/! PW mgr/Sem2/[CV3D] Computer Vision and 3D data processing/proj/data/01_las/chmura_dj.las')
# outlier_remove(lo3d, 30, 2.5)
# outlier_remove(lo3d, 100, 2.0)
# outlier_remove(lo3d, 30, 4.5)


def outlier_remove_sphere(point_cloud, nb_pts=30, r=1.0):
    filtered_point_cloud, ind = point_cloud.remove_radius_outlier(nb_points=nb_pts, radius=r)
    outliers = point_cloud.select_by_index(ind, invert=True)
    print("Draw point clouds - outliers (red colour), point_cloud (RGB): ")
    outliers.paint_uniform_color([1, 0, 0])
    o3d.visualization.draw_geometries([filtered_point_cloud, outliers])
    return filtered_point_cloud, outliers


outlier_remove_sphere(lo3d, 10, 0.7)
