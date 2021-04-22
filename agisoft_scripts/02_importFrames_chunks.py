from glob import glob

doc = Metashape.app.document
files = glob("C:/Users/Mateusz/CV3D/agisoft_scripts/frames/*.jpg")
for i in range(len(files)-1):
    print("Processing {0} / {1}".format(i+1, len(files)-1))
    chunk = doc.addChunk()
    if i == 0:
        chunk.addPhotos(files[0:100])
    else:
        chunk.addPhotos(files[(i*100-10):(i+1)*100])
    chunk.matchPhotos(downscale=1, generic_preselection=True, reference_preselection=False)
    chunk.alignCameras()
print(Metashape.app.document.chunks[0].cameras[0].calibration.k1)
