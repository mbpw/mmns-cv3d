# Import LASPy
import laspy
import numpy as np


# Read the Las file function
file = "D:/! PW mgr/Sem2/[CV3D] Computer Vision and 3D data processing/proj/data/01_las/chmura_dj.las"
las_pcd = laspy.file.File(file, header=None, mode="rw")
X = las_pcd.x
Y = las_pcd.y
Z = las_pcd.z

# Store x,y,z coordinates into the NumPy array
las_points = np.vstack((las_pcd.x, las_pcd.y, las_pcd.z)).transpose()
# # Get and print elements in header
# headerformat = las_pcd.header.header_format
# for spec in headerformat:
#     print(spec.name)
#
# x_max = las_pcd.header.max
# print(x_max)
# las_pcd.header.max = [100000, 100000, 100000]
# offset = las_pcd.header.offset
# print(offset)

# Get access to the point values
pointformat = las_pcd.point_format
for spec in pointformat:
    print(spec.name)

# RGB values normalization
r = las_pcd.red / max(las_pcd.red)
g = las_pcd.green / max(las_pcd.green)
b = las_pcd.blue / max(las_pcd.blue)

las_pcd.red = r
