def chunk_alignment(doc):
    doc.alignChunks([doc.chunks[1].key, doc.chunks[2].key, doc.chunks[3].key, doc.chunks[4].key, doc.chunks[5].key,
                     doc.chunks[6].key], doc.chunks[0].key, method="points")  # , fix_scale=False)
    doc.mergeChunks()
