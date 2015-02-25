#!coding:utf8

from PIL import Image
from PIL.ExifTags import TAGS
import os


class ImagePaser():
    def __init__(self, file):
        self.file = file
        self.fp = file
        self.data = None
        self.width = -1
        self.height = -1
        self.filesize = -1
        self.exif = {}


    def showInfo(self):
        exif = self.parseExif()
        for k,v in exif.items() :
            print k,":",v

    def parseExif(self):
        img = Image.open(self.fp)
        ret = {}
        if hasattr( img, '_getexif' ):
            exifinfo = img._getexif()
            if exifinfo != None:
                for tag, value in exifinfo.items():
                    decoded = TAGS.get(tag, tag)
                    if isinstance(value,type("123")):
                        try:
                            value = value.decode()
                        except:
                            value = ""
                    ret[decoded] = value
                self.exif = ret
                return ret
        return {}

    def parseSize(self):
        img = Image.open(self.fp)
        self.width, self.height = img.size


        
if __name__ == "__main__":
    pass