import re
from detection import extracting_contours
from .extracting_names_fro_con import extracting_data_name_contours


class pan_data_extract:
    def __init__(self, text, imgsrc):
        pan_no = re.findall(r"([A-Z]{5}[\d]{3,4}[A-Z]{1,2})", text)
        pan_no = pan_no[0] if pan_no else 'None'
        DOB = re.findall(r"[\d]{2}/[\d]{1,2}/[\d]{4}", text)
        DOB = DOB[0] if DOB else 'None'
        name_image_algo = extracting_contours.extracting_pan_name_image(imgsrc)
        path_name_image = name_image_algo.getting_name_image()
        names = extracting_data_name_contours.names(self, path_name_image)

        self.pan_no = pan_no
        self.DOB = DOB
        self.names = names

    def get_data(self):
        return self.DOB, self.pan_no, self.names
