import sys


def marker_save(chunk):
    file = sys.argv[2]  #
    file_rep = open(file, 'w')
    for marker in chunk.markers:
        print(marker.label)
        for camera in chunk.cameras:
            if camera.enabled == 1:
                point_2D = marker.projections[camera]
                if point_2D is not None:
                    file_rep.write(marker.label)
                    file_rep.write(' ')
                    file_rep.write(camera.label)
                    file_rep.write(' ')
                    file_rep.write('%f ' % marker.projections[camera].coord[0])
                    file_rep.write('%f ' % marker.projections[camera].coord[1])
                    file_rep.write('\n')
    file_rep.close()
