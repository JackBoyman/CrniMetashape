import os
import logging


def getFolderStructure(path):
    psx_files = list()
    roots_w_psx = list()
    for root, dirs, files in os.walk(path):
        for file in files:
            if ".psx" in file:
                psx_files.append(list())
                psx_files[-1].append(root)
                psx_files[-1].append(file)
                roots_w_psx.append(os.path.dirname(root))

    roots_set = set(roots_w_psx)
    roots = list(roots_set)
    no_proj = list()
    for root in roots:
        dirs_in_root = os.listdir(root)
        for dir in dirs_in_root:
            dir_path = os.path.join(root, dir)
            has_psx = False
            for file in  os.listdir(dir_path):
                if ".psx" in file:
                    has_psx = True
            if not has_psx:
                no_proj.append(dir_path)
    for dir in no_proj:
        logging.critical(f"No Metashape Project in: {dir}")
    logging.info(f"FINISHED checking for .psx files. Found {len(no_proj)} projects missing.\n")
    return psx_files

def inputHandler():
    path = input("Input path to Root-folder: ")
    meshRes = input("Define Mesh resolution: ")
    prefix = input("OPTIONAL Define OBJ file name prefix (e.g. Tunnelheading): ")
    suffix = input("OPTIONAL Define OBJ file name suffix (usually == Mesh Resolution: ")
    
    return path, meshRes, prefix, suffix
    

def inputDebug():
    path= r"P:\Roman_Slowenien\MeshRecalc\Data\15_GC_T1_DI"
    meshRes = 100000
    prefix = "prefix"
    suffix = "suffix"
    
    return path, meshRes, prefix, suffix
