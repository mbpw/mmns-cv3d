"""------------------------------------------------------
Author: Mateusz Białek <mateusz.bialek.stud@pw.edu.pl>
Project for Computer Vision and 3D Data Processing course
MMNS, sem. 2, Warsaw University of Technology, 2021
------------------------------------------------------"""
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


# Manual point picking
def manual_point_picking(point_cloud):
    print("Manual point measurement")
    print("The data processing steps:")
    print(" (1.1) Point measurement - shift + left mouse button")
    print(" (1.2) The undo point picking - shift + right mouse button")
    print(" (2) End of measurement - press Q button")
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window(window_name='Manual point picking')
    vis.add_geometry(point_cloud)
    vis.run()  # user picks points
    vis.destroy_window()
    print("The end of measurement")
    print(vis.get_picked_points())
    return vis.get_picked_points()


lo3d = las_to_o3d('data/01_las/chmura_dj.las')
manual_pcd_croppings(lo3d)
