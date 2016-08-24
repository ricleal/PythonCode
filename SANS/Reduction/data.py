#!/usr/bin/env python
# -*- coding: utf-8 -*-
from settings import logger

import sys
import glob
import os.path

import os, sys
import xml.etree.ElementTree as ET


class Data(object):
    def __init__(self, filename):
        if not os.path.exists(filename):
            logger.error("File {} does not exist!".format(filename))
            return
        self._filename = filename
    
    def parse(self):
        logger.info("Parsing: %s"%self._filename)
        tree = ET.parse(self._filename)
        root = tree.getroot()
        xpath = "Header/Instrument"
        elems = root.findall(xpath)
        for elem in elems:
            logger.info("Elem: %s = %s"%(xpath,elem.text))
            setattr(Data, xpath, elem.text)

class BioSans(Data):
    def __init__(self, filename):
        super( BioSans, self ).__init__(filename)
        self._instrument_name = "BioSANS"

def main(argv):
    d = BioSans("/HFIR/CG3/IPTS-17252/exp321/Shared/SVP/Edited_Datafiles/BioSANS_exp321_scan0050_0001.xml")
    d.parse()
    logger.debug(dir(d))


if __name__ == "__main__":
    main(sys.argv)
    logger.info("Done!")
