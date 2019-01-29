import cv2
from PIL import Image
import pytesseract
import numpy as np
import matplotlib.pyplot as plt
import imutils
import os

min_angle = 82
max_angle = 106.3
min_pixel_Den = 284
max_pixel_Den = 343

pan_DL_cor_min = 87
pan_DL_cor_max = 157

pan_he_min = 14
pan_he_max = 32
pan_max_x_coor = 140
Dl_he_min = 13
Dl_he_max = 18
Dl_width_max = 260


EXTRACTED_SIGN_IMAGE_FOLDER = os.path.join('ori_ext', 'extracted_img')
EXTRACTED_PAN_NAME_IMAGE_FOLDER = os.path.join(
    'ori_ext', 'extracted_pan_name_img')
EXTRACTED_DL_NAME_IMAGE_FOLDER = os.path.join(
    'ori_ext', 'extracted_DL_name_img')


def contour_key(contour):
    rect = cv2.minAreaRect(contour)
    w, h = rect[1]
    if w < h:
        w, h = h, w
    if h > 0 and w/h < 1.5:
        return 0
    else:
        return w * h


# Load the image,resizing and preprocessing

class extracting_contours:
    def __init__(self, imgsrc):
        size = 690, 374
        img_to_extract = Image.open(imgsrc)
        img_extract_resize = img_to_extract.resize(size, Image.ANTIALIAS)
        img_extract_resize.save("img_extract_resize.png", "PNG")
        img_extract_re = Image.open("img_extract_resize.png")
        img_extract_converted = img_extract_re.convert('RGBA')
        basewidth = 670
        wpercent = (basewidth/float(img_extract_converted.size[0]))
        hsize = int((float(img_extract_converted.size[1])*float(wpercent)))
        img_extract_last_resize = img_extract_converted.resize(
            (basewidth, hsize), Image.ANTIALIAS)
        img_extract_last_resize.save('resized_img.png')
        image_extract_to = cv2.imread('resized_img.png')
        gray_image_extract = cv2.cvtColor(image_extract_to, cv2.COLOR_BGR2GRAY)
        gray_image_extract = cv2.medianBlur(gray_image_extract, 5)
        self.gray_image_extract = gray_image_extract
        self.image_extract_to = image_extract_to

    def image_resizing(self):
        return self.gray_image_extract, self.image_extract_to


# extracting contours
class extracting_contours_ext_img(extracting_contours):

    def __init__(self, imgsrc, gray_image_extract):
        ret, binary_image_extract = cv2.threshold(
            gray_image_extract, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        kernel = np.ones((3, 3), np.uint8)
        ext_image_closed = cv2.morphologyEx(
            binary_image_extract, cv2.MORPH_CLOSE, kernel)
        ext_image_open = cv2.morphologyEx(
            ext_image_closed, cv2.MORPH_OPEN, kernel)
        kernel = np.ones((2, 2), np.uint8)
        ext_image_dilate = cv2.erode(ext_image_open, kernel, 3)
        ext_image_not = cv2.bitwise_not(ext_image_dilate)
        ext_image_not_adapt = cv2.adaptiveThreshold(
            ext_image_not, 255, cv2.ADAPTIVE_THRESH_MEAN_C,  cv2.THRESH_BINARY, 15, -2)
        extracted_image_dilate = cv2.dilate(
            ext_image_not_adapt, np.ones((2, 1)))
        extracted_image_dilate = cv2.dilate(
            extracted_image_dilate, np.ones((1, 19)))
        image, ext_img_contours, heirarchy = cv2.findContours(
            extracted_image_dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.ext_img_contours = ext_img_contours

    def extracting_contours_images(self):
        return self.ext_img_contours


# filtering contours


class extracting_sign_contour(extracting_contours):
    def __init__(self, imgsrc, contours, cust_img):
        contours = sorted(contours, key=contour_key, reverse=True)[:10]
        idx = 0
        rgb = 0
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)
            hull = cv2.convexHull(contour, returnPoints=False)
            defects = cv2.convexityDefects(contour, hull)
            roi = cust_img[y:y+h, x:x+w]
            ap = float(w)/h
            me = cv2.mean(roi)
            rgb += me[0]+me[1]+me[2]
            (x, y), (MA, ma), angle = cv2.fitEllipse(contour)
            if(min_angle <= angle <= max_angle and min_pixel_Den < y < max_pixel_Den):
                idx += 1
                filename = str(idx)+'.jpg'
                cv2.imwrite(os.path.join(
                    EXTRACTED_SIGN_IMAGE_FOLDER, filename), roi)
        self.path = os.path.join(EXTRACTED_SIGN_IMAGE_FOLDER, '1.jpg')

    def extracting_sign_image(self,):
        return self.path


class extracting_pan_name_contours(extracting_contours):
    def __init__(self, imgsrc, contours, cust_img):
        contours = sorted(contours, key=contour_key, reverse=True)[:15]
        myContours = []
        idx = 0
        for contour in contours:
            rectangle = cv2.boundingRect(contour)
            myContours.append(rectangle)
        mycontours = sorted(myContours, key=lambda element: (
            element[0], element[1], element[2], element[3]))
        for cnt in mycontours:
            x, y, w, h = cnt[0], cnt[1], cnt[2], cnt[3]
            if(pan_DL_cor_min < y < pan_DL_cor_max and pan_he_min < h < pan_he_max and x < pan_max_x_coor):
                idx += 1
                roi = cust_img[y:y+h, x:x+w]
                filename = str(idx)+'.jpg'
                cv2.imwrite(os.path.join(
                    EXTRACTED_PAN_NAME_IMAGE_FOLDER, filename), roi)
        self.path = EXTRACTED_PAN_NAME_IMAGE_FOLDER

    def extracting_name_image(self):
        return self.path


class extracting_DL_name_contours(extracting_contours):
    def __init__(self, imgsrc, contours, cust_img):
        extracting_contours.__init__(self, imgsrc)
        contours = sorted(contours, key=contour_key, reverse=True)[:15]
        myContours = []
        idx = 0
        for contour in contours:
            rectangle = cv2.boundingRect(contour)
            myContours.append(rectangle)
        mycontours = sorted(myContours, key=lambda element: (
            element[0], element[1], element[2], element[3]))
        for cnt in mycontours:
            x, y, w, h = cnt[0], cnt[1], cnt[2], cnt[3]
            if(pan_DL_cor_min < y < pan_DL_cor_max and Dl_he_min <= h < Dl_he_max and w < Dl_width_max):
                idx += 1
                roi = cust_img[y:y+h, x:x+w]
                filename = str(idx)+'.jpg'
                cv2.imwrite(os.path.join(
                    EXTRACTED_DL_NAME_IMAGE_FOLDER, filename), roi)
        self.path = EXTRACTED_DL_NAME_IMAGE_FOLDER

    def extracting_name_image(self):
        return self.path


class extracting_sign_image:
    def __init__(self, imgsrc):
        image_resizing_algo = extracting_contours(imgsrc)
        gray_image_extract, image_extract_to = image_resizing_algo.image_resizing()
        extracting_contours_algo = extracting_contours_ext_img(
            imgsrc, gray_image_extract)
        ext_img_contours = extracting_contours_algo.extracting_contours_images()
        sign_contour_ext_algo = extracting_sign_contour(
            imgsrc, ext_img_contours, image_extract_to)
        sign_contour_img_path = sign_contour_ext_algo.extracting_sign_image()
        self.path = sign_contour_img_path

    def getting_sign_img(self):
        return self.path


class extracting_pan_name_image:
    def __init__(self, imgsrc):
        image_resizing_algo = extracting_contours(imgsrc)
        gray_image_extract, image_extract_to = image_resizing_algo.image_resizing()
        extracting_contours_algo = extracting_contours_ext_img(
            imgsrc, gray_image_extract)
        ext_img_contours = extracting_contours_algo.extracting_contours_images()
        pan_name_contour_ext_algo = extracting_pan_name_contours(
            imgsrc, ext_img_contours, image_extract_to)
        sign_contour_img_path = pan_name_contour_ext_algo.extracting_name_image()

        self.path = sign_contour_img_path

    def getting_name_image(self):
        return self.path


class extracting_DL_name_image:
    def __init__(self, imgsrc):
        image_resizing_algo = extracting_contours(imgsrc)
        gray_image_extract, image_extract_to = image_resizing_algo.image_resizing()
        extracting_contours_algo = extracting_contours_ext_img(
            imgsrc, gray_image_extract)
        ext_img_contours = extracting_contours_algo.extracting_contours_images()
        sign_contour_ext_algo = extracting_DL_name_contours(
            imgsrc, ext_img_contours, image_extract_to)
        sign_contour_img_path = sign_contour_ext_algo.extracting_name_image()

        self.path = sign_contour_img_path

    def getting_name_image(self):
        return self.path
