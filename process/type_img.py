from skimage.filters import threshold_local
import cv2
import imutils
import pytesseract
import re

search_words = r"(?:MALE|FEMALE|female|male|Male|Female|Income|INCOME|income|Tax|TAX|tax|Account|DEPARTMENT|PASSPORT|Passport|passport|REPUBLIC|Republic|republic|WORLD|Driving|driving|Driving)"


class image_type:
    def __init__(self, imgsrc):
        image = cv2.imread(imgsrc)
        image = imutils.resize(image, height=550)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        T = threshold_local(gray, 15, offset=14.65, method="gaussian")
        final = (gray > T).astype("uint8") * 255
        text = pytesseract.image_to_string(final)
        print(text)
        img_type_keywords = re.findall(search_words, text)
        img_type_keywords = img_type_keywords[0]
        print(img_type_keywords)
        self.imgsrc = img_type_keywords

    def get_data(self):
        return self.imgsrc
        # return self.imgsrc
