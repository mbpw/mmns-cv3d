"""------------------------------------------------------
Author: Mateusz Białek <mateusz.bialek.stud@pw.edu.pl>
Project for Computer Vision and 3D Data Processing course
MMNS, sem. 2, Warsaw University of Technology, 2021
------------------------------------------------------"""
import open3d as o3d


# Point cloud voxel size downsampling
def voxel_downsampling(point_cloud, voxel_size=0.1):
    voxel_point_cloud = point_cloud.voxel_down_sample(voxel_size=voxel_size)
    print("Draw point cloud in the voxel structure - voxel_size %f: " % voxel_size)
    print("Number of points in cloud: %i" % len(voxel_point_cloud.points))
    o3d.visualization.draw_geometries([voxel_point_cloud])
    return voxel_point_cloud


# Point cloud uniform downsampling
def uniform_downsampling(point_cloud, recduction_every_k_points=10):
    uniform_downsample_pcd = point_cloud.uniform_down_sample(every_k_points=recduction_every_k_points)
    print("Draw point cloud with reduced every %i point: " % recduction_every_k_points)
    print("Number of points in cloud: %i" % len(uniform_downsample_pcd.points))
    o3d.visualization.draw_geometries([uniform_downsample_pcd])
    return uniform_downsample_pcd
