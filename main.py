from skimage import io
import matplotlib.pyplot as plt
import time

from block_artifact_grid import Block_Artifact_Grid

image_path = input('Please input image path:')

image = io.imread(image_path)

img_detector = Block_Artifact_Grid(image)
start_time = time.time()

img_detector.detect()

print("--- %s seconds ---" % (time.time() - start_time))

fig = plt.figure()
ax = fig.add_subplot(1, 2, 1)
plt.imshow(image)
ax.set_title('Before')
plt.colorbar(ticks=[0.1, 0.3, 0.5, 0.7], orientation='horizontal')

ax = fig.add_subplot(1, 2, 2)
plt.imshow(img_detector.result_image)
ax.set_title('After')
plt.colorbar(ticks=[0.1, 0.3, 0.5, 0.7], orientation='horizontal')

plt.savefig('result.jpg')
