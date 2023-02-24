import Metashape
import logging
import os
"""
0. Log events like missing files or dirs or chunks etc.

1. get overview of Path hieracy. Where are the projects and how many subfolder hieracys are there

2. Find all psx projects in hieracy. Save their paths in a list. 

3. Open Project, iterate through chunks, find last mesh, dublicate and decimate mesh, textureize it again and export mesh

"""
class agiProcessor:
    def __init__(self, path, meshRes, prefix, suffix):
        self.path = path
        self.meshRes = meshRes
        self.prefix = prefix
        self.suffix = suffix
        self.doc = self.initDoc()

    def initDoc(self):
        doc = Metashape.Document()
        try:
            doc.open(self.path, ignore_lock=True)
        except Exception:
            logging.info(Exception)
        return doc

    def checkIntegrity(self):
        for chunk in self.doc.chunks:
            logging.info(f"WORKING on Chunk {chunk.label}")
            self.checkModels(chunk)
            pahts_ok = self.checkPhotos( chunk)
            if pahts_ok:
                logging.info("IMAGE PATHS are correct.")
            else:
                self.changePaths(chunk)

        
    def checkModels(self, chunk):
        logging.info("CHECKING Models...")
        if chunk.models == []:
            logging.warning(f"Chunk {chunk.label} has no model.")
        else:
            logging.info(f"Chunk {chunk.label} has {len(chunk.models)} model(s).")

    def checkPhotos(self, chunk):
        logging.info("CHECKING for correct image paths...")
        paths_ok = True
        for camera in chunk.cameras:
            photo_path = camera.photo.path
            if not os.path.isfile(photo_path):
                paths_ok = False
        
        if not paths_ok:
            logging.info("FOUND images with incorrect image paths...")

        return paths_ok
    
    def changePaths(self, chunk):
        subdirs = []
        dirname = os.path.dirname(self.path)
        for file in os.listdir(dirname):
            d = os.path.join(self.path, file)
            if os.path.isdir(d) and ".files" not in d:
                subdirs.append(d)
        for camera in chunk.cameras:
            photo_path = camera.photo.path
            basename_photo = os.path.basename(photo_path)
            dirname_photo = os.path.dirname(photo_path)
            basedirname_photo = os.path.basename(dirname_photo)
            if basedirname_photo in subdirs and not os.path.isfile(photo_path):
                camera.photo.path = os.path.join(dirname,basedirname_photo,basename_photo)
            elif basename_photo in os.listdir(dirname) and not os.path.isfile(photo_path):
                camera.photo.path = os.path.join(dirname, basename_photo)
            else:
                logging.error(f"CAN NOT FIND Image {basename_photo}")
