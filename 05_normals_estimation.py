from tools import read_point_cloud_o3d
import open3d as o3d

pcd = read_point_cloud_o3d(
    "D:/PW_mgr/Sem2/[CV3D] Computer Vision and 3D data processing/proj/data/02_eagle/eagle.points.ply")

pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))