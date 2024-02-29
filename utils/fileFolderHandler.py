# Copyright (c) 2023, Kuronekosan
# This version is still alpha-release
#------------------- THIS FEATURE IS STILL ON DEVELOPMENT -------------------#

import os
import sys

class FileHandler:
    def check(self, path:str = ''):
        return os.path.exists(path)

    def checkFolder(self, path:str = ''):
        if not self.check(path):
            try:
                os.makedirs(path)
                return True
            except Exception as e:
                print("Error Occured on checkFolder function at fileFolderHandler\ndetails: ", e)
                sys.exit(1)
        else:
            return True

    def checkFile(self, path: str = ''):
        if not self.check(path):
            try:
                os.makedirs(path)
                return True
            except Exception as e:
                print("Error Occured on checkFile function at fileFolderHandler\ndetails: ", e)
                sys.exit(1)
        else:
            return True
