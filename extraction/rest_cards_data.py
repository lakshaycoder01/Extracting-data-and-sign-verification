from card_data_files import DL_data, pan_data, passport_data
from .faces_sign_call import compare_faces, compare_sign
import abc
import json


class passport_text_extractor(object):
    def extraction(self, textlast, ImgPathExt, person_name):
        Passport_class = passport_data.extract_data(textlast)
        Passport_No, country_name, person_list = Passport_class.get_data()
        face_compare_class = compare_faces(ImgPathExt, person_name)
        face_data = face_compare_class.get_data()
        return json.dumps({'passport_no': Passport_No, 'Country_Name': country_name, 'Name': person_list, 'face_data': face_data})


class DL_text_extractor(object):
    def extraction(self, textlast, ImgPathExt, person_name):
        DL_data_cls = DL_data.extract_DL_no_dates(textlast, ImgPathExt)
        DL_no, Issue_date, dob, name = DL_data_cls.get_data()
        sign_compare_class = compare_sign(ImgPathExt, person_name)
        sign_data = sign_compare_class.get_data()
        face_compare_class = compare_faces(ImgPathExt, person_name)
        face_data = face_compare_class.get_data()
        return json.dumps({'DL_no': DL_no, 'Issue_date': Issue_date, 'dob': dob, 'Name': name, 'sign_data': sign_data, 'face_data': face_data})


class pan_text_extractor(object):
    def extraction(self, textlast, ImgPathExt, person_name):
        Pan_class = pan_data.pan_data_extract(textlast, ImgPathExt)
        dob, pan_no, name = Pan_class.get_data()
        print(dob, pan_no, name)
        sign_compare_class = compare_sign(ImgPathExt, person_name)
        sign_data = sign_compare_class.get_data()
        print(sign_data)
        face_compare_class = compare_faces(ImgPathExt, person_name)
        face_data = face_compare_class.get_data()
        return json.dumps({'dob': dob, 'pan_no': pan_no, 'Name': name, 'sign_data': sign_data, 'face_data': face_data})


class Abstract_extractor_factory(object):
    def gen_data(self):
        raise NotImplementedError("No internal factory that is extracted")


class get_pan_extractor(Abstract_extractor_factory):
    def get_data(self):
        return pan_text_extractor()


class get_passport_extractor(Abstract_extractor_factory):
    def get_data(self):
        return passport_text_extractor()


class get_DL_extractor(Abstract_extractor_factory):
    def get_data(self):
        return DL_text_extractor()


ext_data_text = [{'command': ['Income', 'INCOME', 'income', 'TAX', 'Tax', 'tax', 'Account', 'DEPARTMENT'], 'pattern':get_pan_extractor()},
                 {'command': ['Passport', 'PASSPORT', 'passport', 'REPUBLIC', 'Republic', 'republic'],
                     'pattern':get_passport_extractor()},
                 {'command': ['Driving', 'DRIVING', 'driving'], 'pattern':get_DL_extractor()}]


class rest_cards_data_cls:
    def __init__(self, textlast, ImgPathExt, person_name, keyword):
        extracted_img_funct_res = [
            x for x in ext_data_text if keyword in x['command']]
        extracted_img_func = extracted_img_funct_res[0]['pattern']
        extracted_img_type = extracted_img_func.get_data()
        extraction_img_data = extracted_img_type.extraction(
            textlast, ImgPathExt, person_name)
        self.extraction_img_data = extraction_img_data

    def get_data(self):
        return self.extraction_img_data
