from detection import extracting_contours, face_image_detect
from comparison import sign_verification, face_comparison
from database_conn import database_config
import json


class compare_sign:
    def __init__(self, ImgPathExt, person_name):
        #pan_card.__init__(self, ImgPathExt)
        sign_img_ext_class = extracting_contours.extracting_sign_image(
            ImgPathExt)
        sign_image_contour_ext_path = sign_img_ext_class.getting_sign_img()
        # sign_compare
        db_coll = database_config()
        db_data = db_coll.find({'name': person_name})
        for doc in db_data:
            sign_image_original_path = doc['sign_image']
            sign_compare_class = sign_verification.sign_comparison(
                sign_image_original_path, sign_image_contour_ext_path)
            sign_data = sign_compare_class.getting_compare_res()
        sign_data = json.loads(sign_data)
        self.sign_data = sign_data

    def get_data(self):
        return self.sign_data


class compare_faces:
    def __init__(self, ImgPathExt, person_name):
        #pan_card.__init__(self, ImgPathExt)
        face_detect_img_class = face_image_detect.detected_image(ImgPathExt)
        face_image_contour_ext_path = face_detect_img_class.detection_results()
        # comparing_face_image
        db_coll = database_config()
        db_data = db_coll.find({'name': person_name})
        for doc in db_data:
            face_image_original_path = doc['face_img']
            compare_class = face_comparison.face_compare(
                face_image_original_path, face_image_contour_ext_path)
            face_data = compare_class.get_compared_results()
        face_data = json.loads(face_data)
        self.face_data = face_data

    def get_data(self):
        return self.face_data
