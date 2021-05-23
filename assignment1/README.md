Computer Vision and 3D Data Processing course, Open3D final assignment

# Introduction

Following project is a part of "Computer Vision and 3D Data Processing" course conducted during 2020/2021 academic year
on Warsaw University of Technology - Mobile Mapping and Navigation Systems speciality on the faculty of Geodesy and
Cartography.

The required program was supposed to perform Point Cloud processing including following steps:

1) The conversion of the point cloud - LAS into the O3D format.
2) The point cloud filtering using the statistical method - please propose input parameters.
3) The PCD downsampling - please suggest input parameters.
4) The initial PCD co-registration by the following methods (in the form of the 4x4 transformation matrix):

   4.1. By manual measurement of points on PCD and registration using the Target-based method.

   4.2. By importing the coordinates of the points from a text file and target-based orientation.

   4.3. By automatic keypoint detection, description and matching based on FPFH descriptor.

   4.4. Hierarchical ICP - ICP downsampling and registration.
5) The final registration of the point clouds using the ICP method together with the statistical analysis of the
   obtained results, i.e. the distance between the point clouds, max, min, avg values, statistical distributions, ...).
6) Combining two point clouds into one file (using the "+" operator).
7) Generating a 3D model in the structure of an irregular triangle mesh.

# Usage

Run MBialek_project1.py

You will see the program's main window which is GUI created in tkinter to simplify the usage of the functions by the
user.

Firstly you need to (1) ***load the point clouds*** using the **[Load]** button. The first row is resembling the
reference point clouds, the second one is the one we want to orient (register). You can navigate to the .las file
via **[...]** button and next preview the chosen file by clicking **[Preview]**. It will not overwrite the current state
of clouds that are already loaded - just visualize the selected .las file from the disk.

After choosing the right files and loading them into memory you can display both of them using **[Visualize both]**
button.

To use the (2) **_filtration function_** enter the desired value in the next row (Remove noise) "std:" **input field**
and then press **[Cloud 1]** or **[Cloud 2]** depending on the cloud you'd like to filter. It will perform noise
filtration using statistical method - for each point the average distance betwen the point and n of nearest neighboursis
calculated and then the points that are further than mean+/-std. parameter multiplied by standard deviation value are
filtrated. The default proposed values are n=100, std. (multiplier)=1.5.

The next possibility is to use (3) ***point cloud downsampling*** which is loading only part of the cloud. In the case
of this program I decided to implement it as a uniform downsampling, which means every k-th point is loaded from each
cloud. The parameter k is changeable in the GUI.

The main part of the program is (4) ***performing point clouds registration*** i.e. transforming one of them (oriented,
cloud 2), so it matches the first one (reference, cloud 1). There are numbers of methods to do this that have been
implemented in this project. Each algorithm returns the information about the resultant *fitness* (the bigger the
better, range between 0 and 1) and *RMSE* (the lower the better).

The fine registration can be performed via (5) ***ICP registration*** using one of three algorithms: PointToPoint,
PointToPlane or ColoredICP. Similarily, we can then obtain statistics of the resultant registration - *fitness* and
*RMSE*.

Lastly, the user can (6) ***combine both clouds*** and (7) ***save the result*** as the new .las file
using **[Save combined cloud]** button or save it as an irregular triangle mesh in .ply format using **[Generate mesh]**
.

___
Of course you can also use each module separately in .py scripts (without GUI). Example code is provided in
___test.py___.

# License

Following code is distributed under the MIT license (see: [LICENSE.md](LICENSE.md)).

&copy; Mateusz Białek 2021