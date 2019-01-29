import numpy as np
import cv2
from PIL import Image, ImageEnhance
import os
from skimage.filters import threshold_local

har_cascade = os.path.basename('haar_cascade')
EXTRACTED_FACE_IMAGE_FOLDER = os.path.join('ori_ext', 'extracted_face_img')


class image:
    def __init__(self, ImgPathExt):
        img = Image.open(ImgPathExt)
        contrast = ImageEnhance.Contrast(img)
        contrasted_img = contrast.enhance(3)
        contrasted_img.save('contrast.jpg')
        img = cv2.imread('contrast.jpg')
        img = cv2.resize(img, (700, 600))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(os.path.join(
            har_cascade, 'haarcascade_frontalface_alt_tree.xml'))
        faces = face_cascade.detectMultiScale(
            gray, 1.3, 4, cv2.CASCADE_SCALE_IMAGE, (20, 20))
        for (x, y, w, h) in faces:
            padding = 30
            img = cv2.rectangle(img, (x, y-padding),
                                (x+w, y+h+padding), 255, 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h+padding, x:x+w]
            filename = 'ak.jpg'
            cv2.imwrite(os.path.join(
                EXTRACTED_FACE_IMAGE_FOLDER, filename), roi_color)
        self.path = os.path.join(EXTRACTED_FACE_IMAGE_FOLDER, filename)

    def detected(self):
        return self.path


class detected_image:
    def __init__(self, imgsrc):
        face_detection_algo = image(imgsrc)
        face_img_path = face_detection_algo.detected()
        self.path = face_img_path

    def detection_results(self):
        return self.path
