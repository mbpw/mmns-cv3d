import open3d as o3d

from tools import las_to_o3d


# Bounding box computation
def bounding_box_computation(point_cloud, type='AxisAlignedBoundingBox'):
    if type == 'AxisAlignedBoundingBox':
        print('Bounding box calculation - oriented to the XYZ coordiante system')
        aabb = point_cloud.get_axis_aligned_bounding_box()
        aabb.color = (1, 0, 0)
        print(aabb)
        o3d.visualization.draw_geometries([point_cloud, aabb], window_name='AxisAlignedBoundingBox')
    else:
        print('Bounding box calculation - oriented to the point cloud')
        obb = point_cloud.get_oriented_bounding_box()
        obb.color = (0, 1, 0)
        print(obb)
        o3d.visualization.draw_geometries([point_cloud, obb], window_name='OrientedBoundingBox')


lo3d = las_to_o3d('D:/! PW mgr/Sem2/[CV3D] Computer Vision and 3D data processing/proj/data/01_las/chmura_dj.las')
bounding_box_computation(lo3d)
