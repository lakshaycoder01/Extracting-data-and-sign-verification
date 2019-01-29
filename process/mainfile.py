from process import type_img, data_ext_based_type
import os
import json

ALLOWED_EXTENSIONS = set(
    ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'tiff', 'tif'])

UPLOAD_FOLDER = os.path.basename('upload_images')


def allowed_file(file):
    file_format = '.' in file and file.rsplit(
        '.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return file_format


class image_files_save:
    def __init__(self, img_to_extract):
        if(img_to_extract and allowed_file(img_to_extract.filename)):
            to_extract_img = img_to_extract.filename.rsplit('.', 1)[0].lower()
            to_extract_img = to_extract_img+'.jpg'
            img_to_extract.save(os.path.join(
                UPLOAD_FOLDER, to_extract_img))
        img_to_extract_path = os.path.join(
            UPLOAD_FOLDER, to_extract_img)
        self.img_to_extract_path = img_to_extract_path

    def save_files(self):
        return self.img_to_extract_path


class image_process_verify:
    def __init__(self, img_file, person_name):
        img_files_save_class = image_files_save(img_file)
        img_to_extract_path = img_files_save_class.save_files()
        # getting image type
        img_type_class = type_img.image_type(img_to_extract_path)
        img_type_keywords = img_type_class.get_data()
        if(img_type_keywords):
            # calling keyword_extraction_class
            extracted_data_class = data_ext_based_type.get_keyword_based_extraction(
                img_type_keywords, img_to_extract_path, person_name)
            extracted_data = extracted_data_class.keyword_based_extr_method()
            self.extracted_data = extracted_data
        else:
            self.extracted_data = json.dumps(
                {'results': "Please Upload a clear image"})

    def processing_image(self):
        return self.extracted_data
