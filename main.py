import numpy as np


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')

    refer = np.array([[310661.30, 4683019.75, 41.13, 1],
                      [310665.15, 4683118.77, 65.76, 1],
                      [310806.25, 4683122.57, 54.26, 1]])
    oriented = np.array([[3.10543046e+05, 4.68295420e+06, 3.71739064e+01, 1],
                         [3.10580646e+05, 4.68304435e+06, 6.31460972e+01, 1],
                         [3.10715147e+05, 4.68299755e+06, 5.10652218e+01, 1]])


    # inverted = np.linalg.inv(np.matrix(reference))
    # R = np.dot(oriented, inverted)
    # print(R)
    def calculate_transformation_from_coords(refer, oriented):
        mean_s = np.mean(refer, 0)
        mean_t = np.mean(oriented, 0)
        ref_zeroed = refer - mean_s
        ori_zeroed = oriented - mean_t
        transposed = np.transpose(ori_zeroed)
        multiplcated = np.matmul(transposed, ref_zeroed)

        # print(multiplcated)
        S = np.eye(4, dtype=np.float64)
        U, D, VT = np.linalg.svd(multiplcated)
        if np.linalg.det(U) * np.linalg.det(np.transpose(VT)) < 0:
            S[-1][-1] = -1

        # print(VT, S)
        R = np.matmul(U, np.matmul(S, VT))
        # R = np.reshape(R, -1)
        R = np.transpose(R)
        t = np.reshape(mean_t, -1) - np.reshape(np.matmul(R, (np.transpose(mean_s))), -1)
        return R, t
