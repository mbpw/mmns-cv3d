"""------------------------------------------------------
Author: Mateusz Białek <mateusz.bialek.stud@pw.edu.pl>
Project for Computer Vision and 3D Data Processing course
MMNS, sem. 2, Warsaw University of Technology, 2021
------------------------------------------------------"""
# Manual target-based registration
import copy

import numpy as np
import open3d as o3d

from tools import manual_point_picking, las_to_o3d


def draw_registered_pcd(ref_point_cloud, oriented_point_cloud, transformation):
    """

    :param ref_point_cloud:
    :param oriented_point_cloud:
    :param transformation:
    :return:
    """
    ori_temp = copy.deepcopy(oriented_point_cloud)
    ref_temp = copy.deepcopy(ref_point_cloud)
    ori_temp.paint_uniform_color([1, 0, 0])
    ref_temp.paint_uniform_color([0, 1, 0])
    ori_temp.transform(transformation)
    o3d.visualization.draw_geometries([ori_temp, ref_temp])


def registration_target_based(ref_point_cloud, oriented_point_cloud, type='Measurement', debug=False, file=None):
    """

    :param ref_point_cloud:
    :param oriented_point_cloud:
    :param type:
    :param debug:
    :param file:
    :return:
    """
    if type == 'Measurement':
        print('Manual target-based registration')
        print('Please measure min. 3 tie point on reference point cloud: ')
        point_ref = manual_point_picking(ref_point_cloud)
        print('Please measure min. 3 tie point on point cloud being oriented: ')
        point_ori = manual_point_picking(oriented_point_cloud)
    elif type == 'File':
        print('Target-based registration based on the file')
        # Check if file is set
        if file is None:
            print("Error! Tie-point list not loaded!")
            return

        # TODO: read from file
        point_ref = [20520, 377117, 1591738]
        point_ori = [3360897, 674034, 2525727]
    elif type == 'DM':
        print('Descriptor matching')
        icp = o3d.pipelines.registration.registration_icp(oriented_point_cloud, ref_point_cloud, 1.0, np.identity(4))
        print(icp)
        trans = icp.transformation
        draw_registered_pcd(ref_point_cloud, oriented_point_cloud, trans)

    if type == 'Measurement' or type == 'File':
        assert (len(point_ref) >= 3 and len(point_ori) >= 3)
        assert (len(point_ref) == len(point_ori))
        corr = np.zeros((len(point_ori), 2))
        corr[:, 0] = point_ori
        corr[:, 1] = point_ref
        print(corr)
        p2p = o3d.pipelines.registration.TransformationEstimationPointToPoint()
        trans = p2p.compute_transformation(oriented_point_cloud, ref_point_cloud, o3d.utility.Vector2iVector(corr))

    """Statistics"""
    evaluation = o3d.pipelines.registration.evaluate_registration(
        oriented_point_cloud, ref_point_cloud, 1.0, np.identity(4))
    print(evaluation)
    evaluation_after = o3d.pipelines.registration.evaluate_registration(
        oriented_point_cloud, ref_point_cloud, 1.0, trans)
    print(evaluation_after)

    if debug is True:
        print(trans)
    draw_registered_pcd(ref_point_cloud, oriented_point_cloud, trans)
    # statistical_analysis(ref_point_cloud, oriented_point_cloud, trans)
    if True:
        oriented_point_cloud.transform(trans)
    return trans, oriented_point_cloud


# ICP registration
def registration_ICP(source, target, threshold=1.0, trans_init=np.identity(4), method='p2p'):
    """
    # The function evaluate_registration calculates two main metrics:
    # 1) fitness, which measures the overlapping area (# of inlier correspondences / # of points in target). The higher the better.
    # 2) inlier_rmse, which measures the RMSE of all inlier correspondences. The lower the better
    # ICP deafult itteration = 30
    """
    print('Pre-registartion evaluation')
    evaluation = o3d.pipelines.registration.evaluate_registration(source, target, threshold, trans_init)
    print(evaluation)
    if method == 'p2p':
        print("ICP <Point to point>")
        reg_p2p = o3d.pipelines.registration.registration_icp(
            source, target, threshold, trans_init,
            o3d.pipelines.registration.TransformationEstimationPointToPoint())
        print(reg_p2p)
        print("Transformation matrix:")
        print(reg_p2p.transformation)
        draw_registered_pcd(source, target, reg_p2p.transformation)
        information_reg_p2p = o3d.pipelines.registration.get_information_matrix_from_point_clouds(
            source, target, threshold, reg_p2p.transformation)
        return reg_p2p.transformation, information_reg_p2p
    elif method == 'p2pl':
        print('Normal computation...')
        source.normals = o3d.utility.Vector3dVector(np.zeros((1, 3)))  # Reset normals
        source.estimate_normals()
        target.normals = o3d.utility.Vector3dVector(np.zeros((1, 3)))  # Reset normals
        target.estimate_normals()
        print("ICP <Point to plane>")
        reg_p2pl = o3d.pipelines.registration.registration_icp(
            source, target, threshold, trans_init,
            o3d.pipelines.registration.TransformationEstimationPointToPlane())
        print(reg_p2pl)
        print("Transformation matrix:")
        print(reg_p2pl.transformation)
        draw_registered_pcd(source, target, reg_p2pl.transformation)
        information_reg_p2pl = o3d.pipelines.registration.get_information_matrix_from_point_clouds(
            source, target, threshold, reg_p2pl.transformation)
        return reg_p2pl.transformation, information_reg_p2pl
    elif method == 'cicp':
        print('Normal computation...')
        source.normals = o3d.utility.Vector3dVector(np.zeros((1, 3)))  # Reset normals
        source.estimate_normals()
        target.normals = o3d.utility.Vector3dVector(np.zeros((1, 3)))  # Reset normals
        target.estimate_normals()
        reg_cicp = o3d.pipelines.registration.registration_colored_icp(source, target, threshold)
        print(reg_cicp)
        print("Transformation matrix:")
        print(reg_cicp.transformation)
        draw_registered_pcd(source, target, reg_cicp.transformation)
        information_reg_cicp = o3d.pipelines.registration.get_information_matrix_from_point_clouds(
            source, target, threshold, reg_cicp.transformation)
        return reg_cicp.transformation, information_reg_cicp
    else:
        print('The ICP method was incorrect')


if __name__ == '__main__':
    print('Starting app...')
    ref = las_to_o3d("../data/01_las/chmura_dj.las")
    ori = las_to_o3d("../data/01_las/chmura_zdjecia_naziemne.las")
    # registration_target_based(ref, ori)
    trans, info = registration_ICP(ref, ori, method='cicp')
    ori.transform(trans)
