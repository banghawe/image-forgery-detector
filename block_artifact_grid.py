from skimage.color import rgb2ycbcr
from skimage.segmentation import slic
from scipy.ndimage.filters import median_filter

from utils import *

class Block_Artifact_Grid():
  def __init__(self, image):
    self.image = image
    self.result_percentage = 0
    self.result_image = []
    self.segments = 70
    self.sigma = 5
    self.color = 'cr'
    self.min_lbl = 0.7
    self.differ_treshold = 50
    self.accum_col = 33
    self.median_filter_size = 3

  def detect(self):
    ycbcr_img = rgb2ycbcr(self.image)

    segmented_img = slic(self.image, n_segments=self.segments, sigma=self.sigma)

    if self.color == 'y':
      chosen_img_layer = ycbcr_img[:, :, 0]
    elif self.color == 'cb':
      chosen_img_layer = ycbcr_img[:, :, 1]
    else:
      chosen_img_layer = ycbcr_img[:, :, 2]

    padded_img_horz = mirror_pad_image(chosen_img_layer, 0, self.accum_col // 2)

    M, N = padded_img_horz.shape

    differ_horz = np.zeros((M, N))
    for i in range(1, M - 1):
      for j in range(N):
        differ_horz[i, j] = 2 * padded_img_horz[i, j] - padded_img_horz[i - 1, j] - padded_img_horz[i + 1, j]

    differ_horz = np.absolute(differ_horz)
    differ_horz = median_filter(differ_horz, size=self.median_filter_size)

    for i in range(1, M - 1):
      for j in range(N):
        if differ_horz[i, j] > self.differ_treshold:
          differ_horz[i, j] = self.differ_treshold

    for j in range(N):
      differ_horz[0, j] = differ_horz[1, j]
      differ_horz[M - 1, j] = differ_horz[M - 2, j]

    summed_horz = sum_fiter_horz(differ_horz, self.accum_col)
    summed_horz_pad = mirror_pad_image(summed_horz, self.accum_col // 2, 0)
    med_vert = median_fiter_vert(summed_horz_pad, self.accum_col)

    edge_horz = summed_horz - med_vert
    edge_horz_pad = mirror_pad_image(edge_horz, self.accum_col // 2, 0)
    med_8step_vert = median_filter_8step_vert(edge_horz_pad, self.accum_col)

    self.result_image = med_8step_vert

    
