"""------------------------------------------------------
Author: Mateusz Białek <mateusz.bialek.stud@pw.edu.pl>
Project for Computer Vision and 3D Data Processing course
MMNS, sem. 2, Warsaw University of Technology, 2021
------------------------------------------------------"""
# The DBSCAN clustering
import matplotlib.pyplot as plt
import open3d as o3d
import numpy as np
from tools import las_to_o3d


def klasteryzacja_DBSCAN(point_cloud, min_distance, min_points, progress=True):
    with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
        classes = np.array(point_cloud.cluster_dbscan(eps=min_distance, min_points=min_points, print_progress=progress))
    no_classes = classes.max() + 1
    print("The DBSCAN algorithm detetcted %i classes" % no_classes)
    colors = plt.get_cmap("tab20")(classes / (classes.max()))
    if classes.max() > 0:
        colors[classes < 0] = 0
        point_cloud.colors = o3d.utility.Vector3dVector(colors[:, :3])
        o3d.visualization.draw_geometries([point_cloud])
        return True
    else:
        return False


lo3d = las_to_o3d('data/01_las/chmura_dj.las')
klasteryzacja_DBSCAN(lo3d, 0.5, 10, False)
