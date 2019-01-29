import json
import pytesseract
import imutils
import cv2
from skimage.filters import threshold_local
from card_data_files import pan_data
from .faces_sign_call import compare_faces, compare_sign


class pan_card:
    def __init__(self, ImgPathExt):
        image = cv2.imread(ImgPathExt)
        image = imutils.resize(image, height=550)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        T = threshold_local(gray, 17, offset=14.65, method="gaussian")
        final = (gray > T).astype("uint8") * 255
        textFound = pytesseract.image_to_string(final)
        text = textFound.split('\n')
        text = [x for x in text if x]
        textlast = ' '.join(text)
        # extracting pan no and DOB
        pan_data_cls = pan_data.pan_data_extract(textlast, ImgPathExt)
        dob, Pan_No, names = pan_data_cls.get_data()
        self.dob = dob
        self.Pan_No = Pan_No
        self.names = names

    def get_data(self):
        return json.dumps({'dob': self.dob, 'Pan_No': self.Pan_No, 'person_list': self.names})


class compare(pan_card):
    def __init__(self, ImgPathExt, person_name):
        sign_compare_class = compare_sign(ImgPathExt, person_name)
        sign_data = sign_compare_class.get_data()
        face_compare_class = compare_faces(ImgPathExt, person_name)
        face_data = face_compare_class.get_data()
        self.sign_data = sign_data
        self.face_data = face_data

    def get_data(self):
        return self.sign_data, self.face_data


class pan_card_extract:
    def __init__(self, ImgPathExt, person_name):
        pan_data = pan_card(ImgPathExt)
        Card_data = pan_data.get_data()
        Card_data = json.loads(Card_data)
        compare_class = compare(ImgPathExt, person_name)
        sign_data, face_data = compare_class.get_data()
        pan_data = json.dumps(
            {'Card Data': Card_data, 'sign_data': sign_data, 'face_data': face_data})
        self.pan_data = pan_data

    def data_extraction(self):
        return self.pan_data
