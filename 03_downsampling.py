import open3d as o3d
from tools import las_to_o3d


# Point cloud downsampling
def pcd_downsampling(point_cloud, voxel_size=0.1):
    voxel_point_cloud = point_cloud.voxel_down_sample(voxel_size=voxel_size)
    print("Draw point cloud in the voxel structure - voxel_size %f: " % voxel_size)
    o3d.visualization.draw_geometries([voxel_point_cloud])
    return voxel_point_cloud


def uniform_downsample(point_cloud, recduction_every_k_points=10):
    uniform_downsample_pcd = point_cloud.uniform_down_sample(every_k_points=recduction_every_k_points)
    print("Draw point cloud with reduced every %i point: " % recduction_every_k_points)
    o3d.visualization.draw_geometries([uniform_downsample_pcd])
    return uniform_downsample_pcd


lo3d = las_to_o3d('D:/! PW mgr/Sem2/[CV3D] Computer Vision and 3D data processing/proj/data/01_las/chmura_dj.las')
# o3d.visualization.draw_geometries([lo3d])
# pcd_downsampling(lo3d, 1)
uniform_downsample(lo3d, 1)
