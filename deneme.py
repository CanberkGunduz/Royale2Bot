import mss
import pyautogui
import numpy as np
import cv2
import time

def detect_and_get_fish(detection_threshold=5000, key_to_press='space'):
    """
    Detects a red object within a specified screen area and simulates a key press when the object disappears (indicating it's time to 'get the fish').

    Parameters:
    - monitor_area: A dictionary with 'top', 'left', 'width', and 'height' keys defining the screen area to monitor.
    - lower_red_hsv: The lower bound of the HSV values to detect the red object.
    - upper_red_hsv: The upper bound of the HSV values to detect the red object.
    - detection_threshold: The threshold for detecting a significant change in red object presence.
    - key_to_press: The key to simulate pressing when the red object is detected to disappear.
    """
    with mss.mss() as sct:
        print("Monitoring for red object. Press Ctrl+C to stop.")
        try:
            while True:
                # Capture the specified area of the screen
                img = np.array(sct.grab({'top': 80, 'left': 460, 'width': 240, 'height': 100}))

                # Convert the image from BGR to HSV
                hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

                # Create a mask that only includes pixels within the specified red HSV range
                mask = cv2.inRange(hsv_img, (0, 169, 157),(10,189 ,237))

                # Use the mask to isolate the red parts of the image
                result_img = cv2.bitwise_and(img, img, mask=mask)

                # Save the original and masked images for inspection
                cv2.imwrite('original_image.jpg', img)
                cv2.imwrite('masked_image.jpg', result_img)

                # Sum the values in the mask to determine the amount of red detected
                red_detected = np.sum(mask)
                print(red_detected)

                # Check if the red object is detected based on the threshold
                if red_detected < detection_threshold:
                    print("Red object possibly underwater, fetching the rod!")
                    # pyautogui.press(key_to_press)  # Simulate the key press to fetch the rod
                    time.sleep(1)  # Wait a bit before continuing to monitor

                time.sleep(0.1)  # Short delay to avoid excessive CPU usage
        except KeyboardInterrupt:
            print("Stopped monitoring.")
detect_and_get_fish()

# import win32gui
# def list_window_names():
#     def winEnumHandler(hwnd, ctx):
#         if win32gui.IsWindowVisible(hwnd):
#             print(hex(hwnd), '"' + win32gui.GetWindowText(hwnd) + '"')
#     win32gui.EnumWindows(winEnumHandler, None)
#
#
# def get_inner_windows(whndl):
#     def callback(hwnd, hwnds):
#         if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
#             hwnds[win32gui.GetClassName(hwnd)] = hwnd
#         return True
#     hwnds = {}
#     win32gui.EnumChildWindows(whndl, callback, hwnds)
#     return hwnds
#
# list_window_names()
