import json
import numpy as np
import pytesseract
import re
import cv2
from PIL import Image
from skimage.filters import threshold_local
from .faces_sign_call import compare_faces


class aadhar_card:
    def __init__(self, ImgPathExt):
        img = Image.open(ImgPathExt)
        img = img.convert('RGBA')
        basewidth = 680
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        pix = img.load()

        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pix[x, y][0] < 89 or pix[x, y][1] < 89 or pix[x, y][2] < 89:
                    pix[x, y] = (0, 0, 0, 255)
                else:
                    pix[x, y] = (255, 255, 255, 255)

        img.save('temp.png')
        text = pytesseract.image_to_string(Image.open('temp.png'))
        gender = re.findall(r"MALE|FEMALE|Female|Male|male|female", text)
        gender = gender[0]
        aadhar_no = re.findall(r"([\d]{4}\W*[\d]{4}\W*[\d]{4})", text)
        aadhar_no = aadhar_no[0]
        self.gender = gender
        self.aadhar_no = aadhar_no

    def get_data(self):
        return json.dumps({'gender': self.gender, 'AadharNo': self.aadhar_no})


class compare(aadhar_card):
    def __init__(self, ImgPathExt, person_name):
        face_compare_class = compare_faces(ImgPathExt, person_name)
        face_data = face_compare_class.get_data()
        self.face_data = face_data

    def get_data(self):
        return self.face_data


class aadhar_card_extract:
    def __init__(self, ImgPathExt, person_name):
        aadhar_card_data = aadhar_data(ImgPathExt)
        Card_data = aadhar_card_data.get_data()
        Card_data = json.loads(Card_data)
        # compare_class=compare(ImgPathExt,person_name)
        # face_data=compare_class.get_data()
        aadhar_data = json.dumps({'Card Data': Card_data})
        self.aadhar_data = aadhar_data

    def data_extraction(self):
        return self.aadhar_data
