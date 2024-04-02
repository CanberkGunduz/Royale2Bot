import cv2
import numpy as np

def pick_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = hsv_img[y, x]

        # you might want to adjust the ranges a bit to get all the red pixels
        upper_bound = np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 40])
        lower_bound = np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])

        print(f"Lower bound HSV values: {lower_bound}")
        print(f"Upper bound HSV values: {upper_bound}")

# Replace 'path_to_your_image.jpg' with the path to the image file you want to analyze
image_path = 'C:\\Users\\Canberk\\Desktop\\lsb.jpg'
img = cv2.imread(image_path)
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

cv2.namedWindow('image')
cv2.setMouseCallback('image', pick_color)

while True:
    cv2.imshow('image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
