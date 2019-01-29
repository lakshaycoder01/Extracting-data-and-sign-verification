from card_data_files import DL_data
import json
from .faces_sign_call import compare_faces, compare_sign
import pytesseract
import re
import imutils
import cv2
from skimage.filters import threshold_local


class Driving_licence:
    def __init__(self, ImgPathExt):
        image = cv2.imread(ImgPathExt)
        image = imutils.resize(image, height=530)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        T = threshold_local(gray, 15, offset=14.64, method="gaussian")
        final = (gray > T).astype("uint8") * 255
        text = pytesseract.image_to_string(final)
        text = text.split('\n')
        text = [x for x in text if x]
        textlast = ' '.join(text)
        DL_data_cls = DL_data.extract_DL_no_dates(textlast, ImgPathExt)
        DL_no, issue_date, dob, names = DL_data_cls.get_data()
        self.DL_no = DL_no
        self.issue_date = issue_date
        self.dob = dob
        self.names = names

    def get_data(self):
        return json.dumps({'DL_no': self.DL_no, 'issue_date': self.issue_date, 'dob': self.dob, 'names': self.names})


class compare(Driving_licence):
    def __init__(self, ImgPathExt, person_name):
        print("hereee")
        sign_compare_class = compare_sign(ImgPathExt, person_name)
        sign_data = sign_compare_class.get_data()
        face_compare_class = compare_faces(ImgPathExt, person_name)
        face_data = face_compare_class.get_data()
        self.sign_data = sign_data
        self.face_data = face_data

    def get_data(self):
        return self.sign_data, self.face_data


class DL_card_extract:
    def __init__(self, ImgPathExt, person_name):
        DL_card_data = Driving_licence(ImgPathExt)
        Card_data = DL_card_data.get_data()
        Card_data = json.loads(Card_data)
        compare_algo = compare(ImgPathExt, person_name)
        sign_data, face_data = compare_algo.get_data()
        DL_data = json.dumps(
            {'Card Data': Card_data, 'sign_data': sign_data, 'face_data': face_data})
        self.DL_data = DL_data

    def data_extraction(self):
        return self.DL_data
