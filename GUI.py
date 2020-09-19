import cv2
import numpy as np

import constants


def nothing(x):
    """Do nothing"""
    pass


class GreenScreenGUIException(Exception):
    pass


class GreenScreenGUI:
    def __init__(self, preview):
        self.show_preview = preview
        self.lower_green = constants.LOWER_GREEN
        self.upper_green = constants.UPPER_GREEN

    def __enter__(self):

        # Define GUI elements
        self.preview_window = 'preview'
        self.control_window = 'control'

        cv2.namedWindow(self.control_window)

        if constants.SHOW_PREVIEW:
            cv2.namedWindow(self.preview_window)

        # create trackbars for color change
        cv2.createTrackbar('R_Min', self.control_window, self.lower_green[0], 255, nothing)
        cv2.createTrackbar('G_Min', self.control_window, self.lower_green[1], 255, nothing)
        cv2.createTrackbar('B_Min', self.control_window, self.lower_green[2], 255, nothing)

        cv2.createTrackbar('R_Max', self.control_window, self.upper_green[0], 255, nothing)
        cv2.createTrackbar('G_Max', self.control_window, self.upper_green[1], 255, nothing)
        cv2.createTrackbar('B_Max', self.control_window, self.upper_green[2], 255, nothing)

        return self

    def update_values(self):
        # Get trackbar positions for RGB balance
        self.lower_green = np.array([cv2.getTrackbarPos('R_Min', self.control_window),
                                     cv2.getTrackbarPos('G_Min', self.control_window),
                                     cv2.getTrackbarPos('B_Min', self.control_window)])

        self.upper_green = np.array([cv2.getTrackbarPos('R_Max', self.control_window),
                                     cv2.getTrackbarPos('G_Max', self.control_window),
                                     cv2.getTrackbarPos('B_Max', self.control_window)])

    def update_preview(self, new_frame):
        if not constants.SHOW_PREVIEW:
            pass
        else:
            cv2.imshow(self.preview_window, new_frame)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup
        cv2.destroyWindow(self.control_window)
        cv2.destroyWindow(self.preview_window)
