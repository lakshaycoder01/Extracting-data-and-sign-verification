
import re
from detection import extracting_contours
from .extracting_names_fro_con import extracting_data_name_contours


class extract_DL_no_dates:
    def __init__(self, text, imgsrc):
        DL_no = re.findall(
            r"(?:[A-Z]{2}|[a-z]{2}|[A-Z]{1}[a-z]{1}|[a-z]{1}[A-Z]{1})[\d]{2}\s?[\d]{11}", text)
        DL_no = DL_no[0] if DL_no else None
        dates = re.findall(
            r"([\d]{1,2})[-.\/]?([\d]{1,2})[-.\/]([\d]{4})", text)
        if(dates is None):
            issue_date = 'None'
            dob = 'None'
        else:
            if(dates[0][2] > dates[1][2]):
                issue_date = dates[0][0]+"/"+dates[0][1]+"/"+dates[0][2]
                dob = dates[1][0]+"/"+dates[1][1]+"/"+dates[1][2]
            else:
                issue_date = dates[1][0]+"/"+dates[1][1]+"/"+dates[1][2]
                dob = dates[0][0]+"/"+dates[0][1]+"/"+dates[0][2]
        name_image_algo = extracting_contours.extracting_DL_name_image(imgsrc)
        path_name_image = name_image_algo.getting_name_image()
        names = extracting_data_name_contours.names(self, path_name_image)
        self.DL_no = DL_no
        self.issue_date = issue_date
        self.dob = dob
        self.names = names

    def get_data(self):
        return self.DL_no, self.issue_date, self.dob, self.names
