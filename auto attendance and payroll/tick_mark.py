import cv2
import numpy as np

# Create a green image
img = np.zeros((512, 512, 3), np.uint8)
img[:] = (0, 255, 0)

# Draw a tick mark
cv2.drawContours(img, [np.array([[100, 300], [200, 400], [400, 200]], dtype=np.int32)], 0, (0, 0, 0), thickness=10)

# Display the image
cv2.imshow('Green Tick', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
