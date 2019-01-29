import json
from .faces_sign_call import compare_faces
import numpy as np
import pytesseract
import imutils
import cv2
from skimage.filters import threshold_local
from card_data_files import passport_data


class passport:
    def __init__(self, ImgPathExt):
        image = cv2.imread(ImgPathExt)
        image = imutils.resize(image, height=690)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        T = threshold_local(gray, 17, offset=14.56, method="gaussian")
        final = (gray > T).astype("uint8") * 255
        textFound = pytesseract.image_to_string(final)
        text = textFound.split('\n')
        text = [x for x in text if x]
        textlast = ' '.join(text)
        passport_data_cls = passport_data.extract_data(textlast)
        Passport_No, Country_name, person_list = passport_data_cls.get_data()
        self.Passport_No = Passport_No
        self.Country_name = Country_name
        self.person_list = person_list

    def get_data(self):
        return json.dumps({'PassportNo': self.Passport_No, 'Country Name': self.Country_name, 'Person list': self.person_list})


class compare(passport):
    def __init__(self, ImaPathExt, person_name):
        face_compare_class = compare_faces(ImgPathExt, person_name)
        face_data = face_compare_class.get_data()
        self.face_data = face_data

    def get_data(self):
        return self.face_data


class passport_extract:
    def __init__(self, ImgPathExt, person_name):
        passport_data = pass_data(ImgPathExt)
        Card_data = passport_data.get_data()
        Card_data = json.loads(Card_data)
        # compare_class=compare(ImgPathExt,person_name)
        # face_data=compare_class.get_data()
        data = json.dumps({'Card Data': Card_data})
        self.data = data

    def data_extraction(self):
        return self.data
