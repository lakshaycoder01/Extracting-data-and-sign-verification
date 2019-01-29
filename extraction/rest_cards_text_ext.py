import json
import numpy as np
import pytesseract
import re
import imutils
import cv2
from skimage.filters import threshold_local
import abc
from .rest_cards_data import rest_cards_data_cls


class text_extraction:
    def __init__(self, ImgPathExt, height, threshold, offset):
        image = cv2.imread(ImgPathExt)
        image = imutils.resize(image, height=height)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        T = threshold_local(gray, threshold, offset=offset, method="gaussian")
        final = (gray > T).astype("uint8") * 255
        text = pytesseract.image_to_string(final)
        text = text.split('\n')
        print(text)
        text = [x for x in text if x]
        textlast = ' '.join(text)
        self.text = textlast

    def get_data(self):
        return self.text


ext_data_comp = [{'command': ['Income', 'INCOME', 'income', 'TAX', 'Tax', 'tax', 'Account', 'DEPARTMENT'], 'pattern_function':{'height': 570, 'threshold': 17, 'offset': 14.65}},
                 {'command': ['Passport', 'PASSPORT', 'passport', 'Republic', 'REPUBLIC', 'respublic', 'WORLD'], 'pattern_function':{
                     'height': 695, 'threshold': 17, 'offset': 13.7}},
                 {'command': ['Driving', 'driving', 'Driving'], 'pattern_function':{
                     'height': 530, 'threshold': 15, 'offset': 14.64}}
                 ]


class rest_cards_extract:
    def __init__(self, ImgPathExt, person_name, keyword):
        extracted_img_data_fac_res = [
            x for x in ext_data_comp if keyword in x['command']]
        extracted_img_data_fac = extracted_img_data_fac_res[0]['pattern_function']
        height = extracted_img_data_fac['height']
        threshold = extracted_img_data_fac['threshold']
        offset = extracted_img_data_fac['offset']
        text_data_cls = text_extraction(ImgPathExt, height, threshold, offset)
        text_data = text_data_cls.get_data()
        data_cls = rest_cards_data_cls(
            text_data, ImgPathExt, person_name, keyword)
        data = data_cls.get_data()
        self.data = data

    def get_rest_cards_data(self):
        return self.data
