from scipy.stats import wasserstein_distance
import numpy as np
from scipy.linalg import norm
from scipy import sum, average
from numpy import dot
from skimage.measure import compare_ssim as ssim
from skimage.filters import threshold_local
from scipy import spatial


class mse_nor_histo:
    def normalize(self, arr):
        rng = arr.max()-arr.min()
        amin = arr.min()
        return (arr-amin)*255/rng

    def mse(self, imageA, imageB):
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])
        return err

    def get_histogram(self, img):
        h, w = img.shape
        hist = [0.0] * 256
        for i in range(h):
            for j in range(w):
                hist[img[i, j]] += 1
        return np.array(hist) / (h * w)


class distance_ssim:
    def manh_dist_cal(self, normalized_ori_img, normalized_ext_img):
        difference = normalized_ori_img-normalized_ext_img
        m_norm = sum(abs(difference))
        z_norm = norm(difference.ravel(), 0)
        return m_norm, z_norm

    def ssim_mse(self, normalized_ori_img, normalized_ext_img):
        m = mse_nor_histo.mse(self, normalized_ori_img, normalized_ext_img)
        (s, diff) = ssim(normalized_ori_img, normalized_ext_img, full=True)
        diff = (diff * 255).astype("uint8")
        return m, s

    def wass_distance(self, bla_whi_ori, bla_whi_ext):
        a_hist = mse_nor_histo.get_histogram(self, bla_whi_ori)
        b_hist = mse_nor_histo.get_histogram(self, bla_whi_ext)
        dist = wasserstein_distance(a_hist, b_hist)
        return dist
