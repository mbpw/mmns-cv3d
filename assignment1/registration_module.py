"""------------------------------------------------------
Author: Mateusz Białek <mateusz.bialek.stud@pw.edu.pl>
Project for Computer Vision and 3D Data Processing course
MMNS, sem. 2, Warsaw University of Technology, 2021
------------------------------------------------------"""
# Manual target-based registration
import copy

import numpy as np
import open3d as o3d

from tools import read_point_cloud_o3d, manual_point_picking, las_to_o3d


def draw_registered_pcd(ref_point_cloud, oriented_point_cloud, transformation):
    ori_temp = copy.deepcopy(oriented_point_cloud)
    ref_temp = copy.deepcopy(ref_point_cloud)
    # ori_temp.paint_uniform_color([1, 0, 0])
    # ref_temp.paint_uniform_color([0, 1, 0])
    ori_temp.transform(transformation)
    o3d.visualization.draw_geometries([ori_temp, ref_temp])


def manual_target_based(ref_point_cloud, oriented_point_cloud, type='Measurement', Debug='False'):
    print('Manual target-based registration')
    # draw_registered_pcd(ref_point_cloud, oriented_point_cloud, np.identity(4))
    if type != 'File':
        print('Please measure min. 3 tie point on reference point cloud: ')
        point_ref = manual_point_picking(ref_point_cloud)
        print('Please measure min. 3 tie point on point cloud being oriented: ')
        point_ori = manual_point_picking(oriented_point_cloud)
    elif type == 'File':
        print('Target-based registration based on the file')
        # Wczytanie chmur punktow w postaci plikow tekstowych
        # Przygotowanie plikow ref i ori
    else:  # Inna metoda
        print('Descriptor matching')
    assert (len(point_ref) >= 3 and len(point_ori) >= 3)
    assert (len(point_ref) == len(point_ori))
    corr = np.zeros((len(point_ori), 2))
    corr[:, 0] = point_ori
    corr[:, 1] = point_ref
    print(corr)
    p2p = o3d.pipelines.registration.TransformationEstimationPointToPoint()
    trans = p2p.compute_transformation(oriented_point_cloud, ref_point_cloud, o3d.utility.Vector2iVector(corr))
    if Debug == 'True':
        print(trans)
    draw_registered_pcd(ref_point_cloud, oriented_point_cloud, trans)
    if True:
        oriented_point_cloud.transform(trans)
    # statistical_analysis(ref_point_cloud, oriented_point_cloud, trans)
    return trans, oriented_point_cloud


if __name__ == '__main__':
    print('Starting app...')
    ref = las_to_o3d("data/01_las/chmura_dj.las")
    ori = las_to_o3d("data/01_las/chmura_zdjecia_naziemne.las")
    manual_target_based(ref, ori)
