import Metashape
from marker_save import marker_save

doc = Metashape.app.document
ch = doc.chunks[0]
marker_save(ch)
