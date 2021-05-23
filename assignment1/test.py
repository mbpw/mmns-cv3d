"""------------------------------------------------------
Author: Mateusz Białek <mateusz.bialek.stud@pw.edu.pl>
Project for Computer Vision and 3D Data Processing course
MMNS, sem. 2, Warsaw University of Technology, 2021
------------------------------------------------------"""
# Libraries
import numpy as np
import open3d as o3d

# Additional tools
from tools import *

# Modules
from mesh_module import *
from outliers_module import *
from downsampling_module import *
from registration_module import *
from visualization_module import *

if __name__ == '__main__':
    cloud1 = "<path_to_your_cloud>"
    cloud2 = "<path_to_your_cloud>"
    pcd1 = las_to_o3d(cloud1)
    pcd2 = las_to_o3d(cloud2)
    visualize_both(cloud1, cloud2)

    # (...)
