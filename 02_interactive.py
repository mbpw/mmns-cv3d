# Function for point cloud cropping
import open3d as o3d
from tools import las_to_o3d


def manual_pcd_croppings(point_cloud):
    print("Function for manual geometry cropping")
    print("The data processing steps:")
    print(" (0) Manual definition of the view point by the mouse or:")
    print(" (0.1) Press 'X' twice to align geometry with direction of x-axis")
    print(" (0.2) Press 'Y' twice to align geometry with direction of y-axis")
    print(" (0.3) Press 'Z' twice to align geometry with direction of z-axis")
    print(" (1) Press 'K' to lock screen and to switch to selection mode")
    print(" (2.1) Drag for rectangle selection or")
    print(" (2.2)or use ctrl + left click for polygon selection")
    print(" (3) Press 'C' to get a selected geometry and to save it")
    print(" (4) Press 'F' to switch to freeview mode")
    o3d.visualization.draw_geometries_with_editing([point_cloud], window_name="Manual point cloud cropping ")


lo3d = las_to_o3d('D:/! PW mgr/Sem2/[CV3D] Computer Vision and 3D data processing/proj/data/01_las/chmura_dj.las')
manual_pcd_croppings(lo3d)
