import Metashape
import logging
import os
import osFunctions as osF
import agisoftFunctions as aF
import sys
from datetime import datetime

"""
IMPORTANT

To get lizences of Agisoft working pleas run:
conda env config vars set RLM_LICENSE=dibitdc.dibit.local:5053 

This is mandatoroy to set the license path for agisoft.

If you have an individual license you might need to point to it by using:
agisoft_LICENSE=XXXX>XXXX>XXXX>XXXX 


"""


def main():
    """ Main program """
    #os.environ["agisoft_LICENSE"] = "port@dibitdc.dibit.local:5053"
    logging.basicConfig(handlers=[
                        logging.FileHandler("Log.log", ),
                        logging.StreamHandler(sys.stdout)],
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%d.%m.%y %H:%M:%S',
                        level=logging.DEBUG)
    
    logging.info("\n\n*********************\nProgram has started.\n*********************\n")



    license_found = Metashape.license.valid
    if not license_found:
        logging.critical("Metashape License not found! Programm can not start.")
        exit()
    else:
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%H%M%S")
    
        path, meshRes, prefix, suffix = osF.inputDebug()
        #OBJ_dir = os.mkdir(os.path.join(path, dt_string+"_OBJs"))
        logging.info("CHECKING for .psx files...")
        psx_projs = osF.getFolderStructure(path)
        
        logging.info("\n###########\nSTARTING to work through projects\n###########\n")
        for proj in psx_projs:
            proj_path = os.path.join(proj[0],proj[1])
            logging.info(f"WORKING on Project: {proj_path}")
            metaProj = aF.agiProcessor(proj_path,meshRes, prefix, suffix)
            metaProj.checkIntegrity()
            del metaProj
            logging.info(f"FINIISHED working on project {os.path.basename(proj_path)}\n")
        
        


if __name__ == "__main__":
    main()


