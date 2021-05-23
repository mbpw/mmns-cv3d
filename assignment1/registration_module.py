"""------------------------------------------------------
Author: Mateusz Białek <mateusz.bialek.stud@pw.edu.pl>
Project for Computer Vision and 3D Data Processing course
MMNS, sem. 2, Warsaw University of Technology, 2021
------------------------------------------------------"""
# Manual target-based registration
import copy

import numpy as np
import open3d as o3d

from tools import manual_point_picking, las_to_o3d, calculate_transformation_from_coords


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


# FPFH descriptor
def descriptor_3D_FPFH(point_cloud, radius_feature=1.0, max_nn=50):
    radius = radius_feature * 5
    print('Descriptor FPFH for radius %.3f and %i nearest neigbour' % (radius_feature, max_nn))
    descriptor_fpfh = o3d.pipelines.registration.compute_fpfh_feature(point_cloud,
                                                                      o3d.geometry.KDTreeSearchParamHybrid(
                                                                          radius=radius_feature, max_nn=max_nn))
    return descriptor_fpfh


# Fast descriptor matching
def descriptor_matching(oriented_point_cloud, ref_point_cloud, ori_fpfh, ref_fpfh, max_distance):
    print('Fast descriptor matching')
    opt = o3d.pipelines.registration.FastGlobalRegistrationOption(iteration_number=100,
                                                                  maximum_correspondence_distance=max_distance)
    reg_result = o3d.pipelines.registration.registration_fast_based_on_feature_matching(oriented_point_cloud,
                                                                                        ref_point_cloud, ori_fpfh,
                                                                                        ref_fpfh,
                                                                                        option=opt)
    return reg_result


# Descriptor matching - RANSAC
def descriptor_matching_RANSAC(oriented_point_cloud, ref_point_cloud, ori_fpfh, ref_fpfh, max_distance):
    print('RANSAC descriptor matching')
    trans = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(oriented_point_cloud,
                                                                                     ref_point_cloud, ori_fpfh,
                                                                                     ref_fpfh, True, max_distance,
                                                                                     o3d.pipelines.registration.TransformationEstimationPointToPoint(
                                                                                         False), 3, [
                                                                                         o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(
                                                                                             0.9),
                                                                                         o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(
                                                                                             max_distance)],
                                                                                     o3d.pipelines.registration.RANSACConvergenceCriteria(
                                                                                         100000, 0.999))
    return trans


def registration_target_based(ref_point_cloud, oriented_point_cloud, type='Measurement', debug=False, file=None,
                              trans_init=np.identity(4), threshold=1.0):
    """

    :param ref_point_cloud:
    :param oriented_point_cloud:
    :param type:
    :param debug:
    :param file:
    :param trans_init
    :param threshold:
    :return:
    """
    """Statistics before"""
    print('Pre-registartion evaluation')
    evaluation = o3d.pipelines.registration.evaluate_registration(ref_point_cloud, oriented_point_cloud, threshold,
                                                                  trans_init)
    print(evaluation)

    trans = trans_init
    if type == 'Measurement':
        print('Manual target-based registration')
        print('Please measure min. 3 tie point on reference point cloud: ')
        point_ref = manual_point_picking(ref_point_cloud)
        print('Please measure min. 3 tie point on point cloud being orient: ')
        point_ori = manual_point_picking(oriented_point_cloud)
    elif type == 'File':
        print('Target-based registration based on the file')
        # Check if file is set
        if file is None:
            print("Error! Tie-point list not loaded!")
            return

        # point_ref = [20520, 377117, 1591738]
        # point_ori = [3360897, 674034, 2525727]
        print("Loading file " + file + "...")
        ff = np.loadtxt(file, dtype=np.float64)
        l = len(ff)
        # print(l)
        refer = np.c_[ff[:, 0:3], np.ones(l)]
        orient = np.c_[ff[:, 3:6], np.ones(l)]
        # orient = ff[:, 3:6]
        print(refer)
        print(orient)

        # for p1 in point_ref:
        #     print(ref_point_cloud.points[p1])
        #
        # for p2 in point_ori:
        #     print(oriented_point_cloud.points[p2])
        #
        # refer = np.array([[3.10661300e+05, 4.68301975e+06, 4.11299993e+01, 1.],
        #                   [3.10665150e+05, 4.68311877e+06, 6.57600003e+01, 1.],
        #                   [3.10806250e+05, 4.68312257e+06, 5.42600002e+01, 1.]])
        # orient = np.array([[3.10543046e+05, 4.68295420e+06, 3.71739064e+01, 1.],
        #                    [3.10580646e+05, 4.68304435e+06, 6.31460972e+01, 1.],
        #                    [3.10715147e+05, 4.68299755e+06, 5.10652218e+01, 1.]])
        # orient = [[310542.718750, 4682953.000000, 39.221931, 1.],
        #             [310619.656250, 4682944.000000, 17.698511, 1.],
        #             [310580.406250, 4683043.000000, 63.092960, 1.],
        #             [310722.562500, 4683028.500000, 18.011694, 1.]]
        # refer = np.array([[310661.250000, 4683019.000000, 41.130001, 1.],
        #                   [310736.656250, 4683037.500000, 22.050001, 1.],
        #                   [310666.062500, 4683118.000000, 65.040001, 1.],
        #                   [310803.031250, 4683154.500000, 20.270000, 1.]])
        R, t = calculate_transformation_from_coords(orient, refer)
        trans = R
        trans[:3, 3] = t[:3]
        # print(trans)

    elif type == 'DM':
        print('Descriptor matching')
        print('Normal computation...')
        ref_point_cloud.normals = o3d.utility.Vector3dVector(np.zeros((1, 3)))  # Reset normals
        ref_point_cloud.estimate_normals()
        oriented_point_cloud.normals = o3d.utility.Vector3dVector(np.zeros((1, 3)))  # Reset normals
        oriented_point_cloud.estimate_normals()
        print('Calculating 3D FPFH descriptors...')
        ori_fpfh = descriptor_3D_FPFH(oriented_point_cloud)
        ref_fpfh = descriptor_3D_FPFH(ref_point_cloud)

        print('Matching descriptors (fast)...')
        reg_result = descriptor_matching(oriented_point_cloud, ref_point_cloud, ori_fpfh, ref_fpfh, max_distance=0.5)
        trans = reg_result.transformation
        # print('Matching descriptors (RANSAC)...')
        # reg_result = descriptor_matching_RANSAC(oriented_point_cloud, ref_point_cloud, ori_fpfh, ref_fpfh,
        #                                         max_distance=0.5)
        # trans = reg_result.transformation

        print(reg_result)
        print(trans)
        # ref_fpfh = o3d.pipelines.registration.compute_fpfh_feature(ref_point_cloud,
        #                                                            o3d.geometry.KDTreeSearchParamHybrid(
        #                                                                radius=threshold, max_nn=100))
        # ori_fpfh = o3d.pipelines.registration.compute_fpfh_feature(oriented_point_cloud,
        #                                                            o3d.geometry.KDTreeSearchParamHybrid(
        #                                                                radius=threshold, max_nn=100))
        # icp = o3d.pipelines.registration.registration_icp(oriented_point_cloud, ref_point_cloud, 1.0, np.identity(4))
        # print(icp)
        # trans = icp.transformation
        # draw_registered_pcd(ref_point_cloud, oriented_point_cloud, trans)

    elif type == "Correspondence":
        point_ref = [20520, 377117, 1591738]
        point_ori = [3360897, 674034, 2525727]

    if type == 'Measurement' or type == 'Correspondence':
        assert (len(point_ref) >= 3 and len(point_ori) >= 3)
        assert (len(point_ref) == len(point_ori))
        corr = np.zeros((len(point_ori), 2))
        corr[:, 0] = point_ori
        corr[:, 1] = point_ref
        print(corr)
        p2p = o3d.pipelines.registration.TransformationEstimationPointToPoint()
        trans = p2p.compute_transformation(oriented_point_cloud, ref_point_cloud, o3d.utility.Vector2iVector(corr))

    """Statistics after"""
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
            o3d.pipelines.registration.TransformationEstimationPointToPoint(),
            o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=2000))
        print(reg_p2p)
        print("Transformation matrix:")
        print(reg_p2p.transformation)
        draw_registered_pcd(source, target, reg_p2p.transformation)
        information_reg_p2p = o3d.pipelines.registration.get_information_matrix_from_point_clouds(
            source, target, threshold, reg_p2p.transformation)
        return reg_p2p.transformation, information_reg_p2p
    elif method == 'p2pl':
        print('Normals computation...')
        source.normals = o3d.utility.Vector3dVector(np.zeros((1, 3)))  # Reset normals
        source.estimate_normals()
        target.normals = o3d.utility.Vector3dVector(np.zeros((1, 3)))  # Reset normals
        target.estimate_normals()
        print("ICP <Point to plane>")
        reg_p2pl = o3d.pipelines.registration.registration_icp(
            source, target, threshold, trans_init,
            o3d.pipelines.registration.TransformationEstimationPointToPlane(),
            o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=2000))
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
    trans, oriented = registration_target_based(ref, ori, "File", file="asd", debug=True)
    # trans, info = registration_ICP(ref, ori, method='cicp')
    #
    # t1 = np.array([[9.34166117e-01, -3.56813086e-01, -4.25294850e-03, 1.69134432e+06],
    #                [3.56835015e-01, 9.34038670e-01, 1.55091979e-02, 1.97940958e+05],
    #                [-1.56146641e-03, -1.60057681e-02, 9.99870680e-01, 7.54383217e+04],
    #                [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
    # # print(t1)
    # draw_registered_pcd(ori, ref, t1)
    #
    # t2 = np.array([[9.34179918e-01, -3.56776960e-01, -4.25222272e-03, 1.69132878e+06],
    #                [3.56798896e-01, 9.34052612e-01, 1.55005293e-02, 1.98092725e+05],
    #                [-1.55843199e-03, -1.59974716e-02, 9.99870818e-01, 7.54034691e+04],
    #                [0., 0., 0., 1.]])
    # draw_registered_pcd(ref, ori, t2)

# ori.transform(trans)
