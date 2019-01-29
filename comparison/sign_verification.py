import cv2
import numpy as np
import json
import os
from .com_tasks import mse_nor_histo, distance_ssim

MIN_MATCH_COUNT = 13
MAX_NORM = 153.9
ZEO_NORM = 38456
MAX_MSE_ERROR = 5.15e-06
MIN_SSIM = .9890
MAX_WASS_DISTANCE = .0018


class compare:
    def __init__(self, imgsrc1, imgsrc2):
        original_img = cv2.imread(imgsrc1)
        ext_img = cv2.imread(imgsrc2)
        original_img_resize = cv2.resize(original_img, (500, 230))
        ext_img_resize = cv2.resize(ext_img, (500, 230))
        gray_original_img = cv2.cvtColor(
            original_img_resize, cv2.COLOR_BGR2GRAY)
        gray_ext_image = cv2.cvtColor(ext_img_resize, cv2.COLOR_BGR2GRAY)

        ret, final_original = cv2.threshold(
            gray_original_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        ret, final_extracted = cv2.threshold(
            gray_ext_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        kernel = np.ones((5, 5), np.uint8)
        dilated_original_img = cv2.erode(final_original, kernel, iterations=1)

        sift = cv2.xfeatures2d.SIFT_create()
        matcher = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), {})
        kpts1, descs1 = sift.detectAndCompute(dilated_original_img, None)
        kpts2, descs2 = sift.detectAndCompute(final_extracted, None)
        matches = matcher.knnMatch(descs1, descs2, 2)
        matches = sorted(matches, key=lambda x: x[0].distance)
        good_points = [
            m1 for (m1, m2) in matches if m1.distance < 0.7 * m2.distance]
        self.good_points = len(good_points)
        self.dilated_original_img = dilated_original_img
        self.final_extracted = final_extracted

    def sign_comparison(self):
        return self.good_points, self.dilated_original_img, self.final_extracted


class distance_cal(compare):
    def __init__(self, bla_whi_ori, bla_whi_ext):
        mse_nor_histo_object = mse_nor_histo()

        original_image_normalized = mse_nor_histo_object.normalize(bla_whi_ori)
        extracted_image_normalized = mse_nor_histo_object.normalize(
            bla_whi_ext)
        distance_algo = distance_ssim()

        m_norm, z_norm = distance_algo.manh_dist_cal(
            original_image_normalized, extracted_image_normalized)
        mean_error, struct_simi = distance_algo.ssim_mse(
            original_image_normalized, extracted_image_normalized)
        wass_distance_cal = distance_algo.wass_distance(
            bla_whi_ori, bla_whi_ext)

        self.m_norm = m_norm
        self.z_norm = z_norm
        self.mean_error = mean_error
        self.struct_simi = struct_simi
        self.wass_distance_cal = wass_distance_cal

    def sign_comparison(self):
        return self.m_norm, self.z_norm, self.mean_error, self.struct_simi, self.wass_distance_cal


class sign_comparison:
    def __init__(self, imgsrc1, imgsrc2):
        good_points_sift_algo = compare(imgsrc1, imgsrc2)

        good_points, bla_whi_ori, bla_whi_ext = good_points_sift_algo.sign_comparison()
        distance_algo = distance_cal(bla_whi_ori, bla_whi_ext)
        m_norm, z_norm, mean_error, struct_simi, wass_distance_cal = distance_algo.sign_comparison()
        if(good_points > MIN_MATCH_COUNT and m_norm < MAX_NORM and z_norm < ZEO_NORM and mean_error < MAX_MSE_ERROR and struct_simi > MIN_SSIM and wass_distance_cal < MAX_WASS_DISTANCE):

            data = json.dumps({'Message': "Signature are matched. You can proceed further",
                               'OriginalSignpath': imgsrc1, 'ExtractedSignpath': imgsrc2})
            print("Data Returned")
        else:
            data = json.dumps({'Message': "Signature aren't matched. Please upload authentic signature",
                               'OriginalSignpath': imgsrc1, 'ExtractedSignpath': imgsrc2})
        self.data = data

    def getting_compare_res(self):
        return self.data
