import sys
from glob import glob
import Metashape
# import xml.dom.minidom as x

# def read_xml(file):
#     dom = x.parse(file)
#     f = dom.f
#     cx = dom.cx
#     cy = dom.cy
#     k1 = dom.k1
#     k2 = dom.k2
#     dom.k3
#     dom.p1
#     dom.p2
#     dom.date
#     return


def load_images():
    doc = Metashape.app.document
    chunk = doc.addChunk()
    files = glob("C:/Users/Mateusz/CV3D/agisoft_scripts/frames/*.jpg")
    print(f"total: {len(files)}")
    for i in range(len(files) - 1):
        print("Processing {0} / {1}".format(i + 1, len(files) - 1))
        if i != 0 and i % 50 == 0:
            chunk = doc.addChunk()
        chunk.addPhotos([files[i]])
        if i >= 149:  # stop adding more photos to save time
            break


def io_import():
    chunk = Metashape.app.document.chunks[0]
    print('chunk: ', chunk)
    sensor = chunk.addSensor()
    sensor.label = 'GoPro'
    sensor.type = Metashape.Sensor.Type.Frame
    sensor.width = 3840
    sensor.height = 2160
    sensor.pixel_width = 0.0016
    sensor.pixel_height = 0.0016
    sensor.focal_length = 2.98
    calib = Metashape.Calibration()
    calib.load("C:\\Users\\Mateusz\\Downloads\\chunk_0_calibration.xml")
    sensor.user_calib = calib
    for camera in chunk.cameras:
        camera.sensor = sensor
    pass


Metashape.app.removeMenuItem("Load images")
Metashape.app.removeMenuItem("Orientation")

Metashape.app.addMenuItem("Load images", load_images)
Metashape.app.addMenuItem("Orientation/Import IO", io_import)
