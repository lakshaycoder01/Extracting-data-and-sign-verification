import re
import cv2
from PIL import Image
import numpy as np
import pytesseract
import imutils
from skimage.filters import threshold_local
import os


class extracting_data_name_contours:
    def names(self, path):
        text_col = []
        for img in os.listdir(path):
            img = Image.open(os.path.join(path, img))
            img = img.convert('RGBA')
            basewidth = 545
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth, hsize), Image.ANTIALIAS)
            img.save('rame.png')
            pix = img.load()
            for y in range(img.size[1]):
                for x in range(img.size[0]):
                    if pix[x, y][0] < 83 or pix[x, y][1] < 85.5 or pix[x, y][2] < 88:
                        pix[x, y] = (0, 0, 0, 255)
                    else:
                        pix[x, y] = (255, 255, 255, 255)
            img.save('name.png')

            text = pytesseract.image_to_string(Image.open('name.png'))
            text_col.append(text)
        text = [re.sub('[^a-zA-Z]+', ' ', tex) for tex in text_col]
        text = [tex for tex in text if len(tex) > 1]
        return text
