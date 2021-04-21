"""------------------------------------------------------
Author: Mateusz Białek <mateusz.bialek.stud@pw.edu.pl>
Project for Computer Vision and 3D Data Processing course
MMNS, sem. 2, Warsaw University of Technology, 2021
------------------------------------------------------"""
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
from tools import read_point_cloud_o3d


# Poisson surface reconstruction
def normals_estimation(point_cloud):
    print("Point cloud vertex normals estimation")
    point_cloud.normals = o3d.utility.Vector3dVector(np.zeros((1, 3)))  # If normals exist, then are removed
    return point_cloud.estimate_normals()


def poisson_reconstruction(point_cloud):
    print("Poisson reconstruction")
    # normals_estimation(point_cloud)
    with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
        tin, density = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd=point_cloud, depth=8)
        print(tin)
        o3d.visualization.draw_geometries([tin])
        return tin, density


# Mesh density visualization
def mesh_density(density, tin):
    density = np.asarray(density)
    density_colors = plt.get_cmap('plasma')(
        (density - density.min()) / (density.max() - density.min()))
    density_colors = density_colors[:, :3]
    density_mesh = o3d.geometry.TriangleMesh()
    density_mesh.vertices = tin.vertices
    density_mesh.triangles = tin.triangles
    density_mesh.triangle_normals = tin.triangle_normals
    density_mesh.vertex_colors = o3d.utility.Vector3dVector(density_colors)
    o3d.visualization.draw_geometries([density_mesh])


# TIN filtration based on the density
def density_tin_filtration(tin, density, quantile=0.01):
    print("Remove low density verticies")
    vertices_to_remove = density < np.quantile(density, quantile)
    tin.remove_vertices_by_mask(vertices_to_remove)
    print(tin)
    o3d.visualization.draw_geometries([tin])


def poisson_filtration(point_cloud):
    tin, density = poisson_reconstruction(point_cloud)
    mesh_density(density, tin)
    density_tin_filtration(tin, density, quantile=0.01)
    o3d.io.write_triangle_mesh("poisson_model.ply", tin)


if __name__ == '__main__':
    pcd = read_point_cloud_o3d(
        "data/02_eagle/eagle.points.ply")
    poisson_filtration(pcd)
