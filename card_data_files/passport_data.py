
import datefinder
import re


class extract_data:
    def __init__(self, text):
        print(text)
        Passport_no = re.findall(r"[A-Z]{1}[\d]{7}", text)
        Passport_no = Passport_no[0] if Passport_no else 'None'
        dates = re.findall(r"[0-9]{2}/[\d]{1,2}/[\d]{4}", text)

    def get_data(self):
        return self.Passport_no, self.count_names, self.person_list
