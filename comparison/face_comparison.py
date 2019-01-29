import cv2
import numpy as np
from skimage.filters import threshold_local
import json
from .com_tasks import mse_nor_histo, distance_ssim
import os


MIN_MATCH_COUNT = 50
MAX_NORM = 92.5
ZEO_NORM = 23300
MAX_MSE_ERROR = 1.50e-06
MIN_SSIM = .991
MAX_WASS_DISTANCE = .00047


class compare:
    def __init__(self, imgsrc1, imgsrc2):
        img1 = cv2.imread(imgsrc1)
        img2 = cv2.imread(imgsrc2)
        img1 = cv2.resize(img1, (500, 500))
        img2 = cv2.resize(img2, (500, 500))
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        T1 = threshold_local(gray1, 17, offset=14.4, method="gaussian")
        final1 = (gray1 > T1).astype("uint8") * 255
        T2 = threshold_local(gray2, 17, offset=14.4, method="gaussian")
        final2 = (gray2 > T2).astype("uint8") * 255
        sift = cv2.xfeatures2d.SURF_create()

        matcher = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), {})
        kpts1, descs1 = sift.detectAndCompute(final1, None)
        kpts2, descs2 = sift.detectAndCompute(final2, None)
        matches = matcher.knnMatch(descs1, descs2, 2)
        matches = sorted(matches, key=lambda x: x[0].distance)
        print("lakshay")
        good_points = [
            m1 for (m1, m2) in matches if m1.distance < 0.7 * m2.distance]
        print(len(good_points))
        self.good_points = len(good_points)
        self.bla_whi_ori = final1
        self.bla_whi_ext = final2

    def face_comparison(self):
        return self.good_points, self.bla_whi_ori, self.bla_whi_ext


class distance_cal(compare):
    def __init__(self, imgsrc1, imgsrc2, bla_whi_ori, bla_whi_ext):
        compare.__init__(self, imgsrc1, imgsrc2)
        mse_nor_histo_object = mse_nor_histo()
        original_image_normalized = mse_nor_histo_object.normalize(bla_whi_ori)
        extracted_image_normalized = mse_nor_histo_object.normalize(
            bla_whi_ext)
        distance_Algo = distance_ssim()
        m_norm, z_norm = distance_Algo.manh_dist_cal(
            original_image_normalized, extracted_image_normalized)
        mean_error, struct_simi = distance_Algo.ssim_mse(
            original_image_normalized, extracted_image_normalized)

        wass_distance_cal = distance_Algo.wass_distance(
            bla_whi_ori, bla_whi_ext)
        self.m_norm = m_norm
        self.z_norm = z_norm
        self.mean_error = mean_error
        self.struct_simi = struct_simi
        self.wass_distance_cal = wass_distance_cal

    def face_comparison(self):
        return self.m_norm, self.z_norm, self.mean_error, self.struct_simi, self.wass_distance_cal


class face_compare:
    def __init__(self, imgsrc1, imgsrc2):
        good_points_sift_algo = compare(imgsrc1, imgsrc2)
        good_points, bla_whi_ori, bla_whi_ext = good_points_sift_algo.face_comparison()
        distance_algo = distance_cal(
            imgsrc1, imgsrc2, bla_whi_ori, bla_whi_ext)
        m_norm, z_norm, mean_error, struct_simi, wass_distance_cal = distance_algo.face_comparison()
        if(good_points > MIN_MATCH_COUNT and m_norm < MAX_NORM and z_norm < ZEO_NORM and mean_error < MAX_MSE_ERROR and wass_distance_cal < MAX_WASS_DISTANCE):

            data = json.dumps({'Message': "Faces are matched. You can proceed further",
                               'OriginalFacepath': imgsrc1, 'ExtractedFacepath': imgsrc2})
        else:
            data = json.dumps({'Message': "Faces aren't matched. Please upload authentic face picture",
                               'OriginalFacepath': imgsrc1, 'ExtractedFacepath': imgsrc2})
        self.data = data

    def get_compared_results(self):
        return self.data
