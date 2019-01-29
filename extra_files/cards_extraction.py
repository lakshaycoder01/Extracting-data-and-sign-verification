import json
from sig_verify import sign_compare
from sig_verify import extracting_sign_image
import numpy as np
import pytesseract
import re
import imutils
import cv2
from skimage.filters import threshold_local


def DL_card_extract(ImgPathExt, ImgPathOri):
    image = cv2.imread(ImgPathExt)
    image = imutils.resize(image, height=530)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    T = threshold_local(gray, 15, offset=14.64, method="gaussian")
    final = (gray > T).astype("uint8") * 255
    text = pytesseract.image_to_string(final)
    text = text.split('\n')
    text = [x for x in text if x]
    textlast = ' '.join(text)
    DL_no, issue_date, dob = extract_DL_no_dates(textlast)
    sign_image_contour_ext_path = extracting_sign_image(ImgPathExt)
    data = sign_compare(ImgPathOri, sign_image_contour_ext_path)
    data = json.loads(data)


def passport_extract(ImgPathExt, ImgPathOri):
    image = cv2.imread(ImgPathExt)
    image = imutils.resize(image, height=690)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    T = threshold_local(gray, 17, offset=14.56, method="gaussian")
    final = (gray > T).astype("uint8") * 255
    textFound = pytesseract.image_to_string(final)
    text = textFound.split('\n')
    text = [x for x in text if x]
    textlast = ' '.join(text)
    Passport_No, Country_name = extract_pass_no_country(textlast)
    print(Passport_No, Country_name)
    person_list = get_names_pass(textlast)
    data = json.dumps({'Passport_No': Passport_No,
                       'Country_name': Country_name, 'person': person_list})
    return data
