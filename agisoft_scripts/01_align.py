doc = Metashape.app.document
chunk = doc.chunk
chunk.matchPhotos(downscale=1, generic_preselection=True, reference_preselection=False)
chunk.alignCameras()