from extraction import rest_cards_text_ext, aadhaar_data_ext
import abc


class rest_cards_extractor(object):
    def extraction(self, ImgPathExt, person_name, keywords):
        Rest_cards_class = rest_cards_text_ext.rest_cards_extract(
            ImgPathExt, person_name, keywords)
        return Rest_cards_class.get_rest_cards_data()


class aadhar_extractor(object):
    def extraction(self, ImgPathExt, person_name, keywords):
        Aadhar_class = aadhaar_data_ext.aadhar_card_extract(
            ImgPathExt, person_name)
        return Aadhar_class.data_extraction()


class Abstract_extractor_factory(object):
    def gen_data(self):
        raise NotImplementedError()


class get_rest_cards_extractor(Abstract_extractor_factory):
    def get_data(self):
        print("coming hereeee")
        return rest_cards_extractor()


class get_aadhar_extractor(Abstract_extractor_factory):
    def get_data(self):
        return aadhar_extractor()


ext_data = [{'command': ['Income', 'INCOME', 'income', 'TAX', 'Tax', 'tax', 'DEPARTMENT', 'Account', 'Passport', 'PASSPORT', 'REPUBLIC', 'Republic', 'republic', 'passport', 'Driving', 'driving', 'Driving'], 'pattern_function':get_rest_cards_extractor()},
            {'command': ['Male', 'Female', 'MALE', 'FEMALE', 'male', 'female', 'Governmen'], 'pattern_function':aadhar_extractor()}]


class get_keyword_based_extraction:
    def __init__(self, keyword, ImgPathExt, person_name):
        extracted_img_funct_res = [
            x for x in ext_data if keyword in x['command']]
        extracted_img_func = extracted_img_funct_res[0]['pattern_function']
        extracted_img_type = extracted_img_func.get_data()
        extraction_img_data = extracted_img_type.extraction(
            ImgPathExt, person_name, keyword)
        self.extraction_img_data = extraction_img_data
        print(self.extraction_img_data)

    def keyword_based_extr_method(self):
        return self.extraction_img_data
