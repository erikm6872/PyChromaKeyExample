import cv2
import numpy as np
from PIL import Image
import pyscreenshot as ImageGrab

import constants


# Global variables
lower_green = constants.LOWER_GREEN
upper_green = constants.UPPER_GREEN

signal_height = None
signal_width = None


def green_screen(frame, background_image):
    """Chroma key method."""
    img = np.copy(frame)

    # Create an image mask to change green pixels to black
    mask = cv2.inRange(img, lower_green, upper_green)

    masked_image = np.copy(img)
    masked_image[mask != 0] = [0, 0, 0]

    # Create another image mask to turn non-green pixels black on the background image
    try:
        background_image = cv2.cvtColor(background_image, cv2.COLOR_BGR2RGB)
    except cv2.error as c:
        # This error occurs when the background video ends and does not restart.
        # TODO: FIX THIS BUG
        print("CV2 Error: " + repr(c))
        background_image = cv2.imread(constants.BACKGROUND_VIDEO_ERROR_PATH)
        masked_image = cv2.imread(constants.BACKGROUND_VIDEO_ERROR_PATH)
        masked_image = cv2.resize(masked_image, (signal_width, signal_height))

    crop_background = None
    try:
        crop_background = cv2.resize(background_image, (signal_width, signal_height))    #background_image[0:signal_height, 0:signal_width]
        crop_background[mask == 0] = [0, 0, 0]
    except cv2.error:
        # Debugging. `background_image` is null when bg video ends. If this happens, print error message and crash.
        print("image=" + repr(background_image) + " width=" + repr(signal_width) + " height=" + repr(signal_height))
        exit(0)

    return np.array(masked_image + crop_background)


def capture_background(bounds):
    """Captures a portion of the computer screen"""
    im = ImageGrab.grab(bbox=bounds)
    return im


def nothing(x):
    """Do nothing"""
    pass


def main():
    """Main program loop"""
    global lower_green, upper_green, signal_height, signal_width

    # Define GUI elements
    preview_window = 'preview'
    control_window = 'control'
    cv2.namedWindow(preview_window)
    cv2.namedWindow(control_window)

    # create trackbars for color change
    cv2.createTrackbar('R_Min', control_window, lower_green[0], 255, nothing)
    cv2.createTrackbar('G_Min', control_window, lower_green[1], 255, nothing)
    cv2.createTrackbar('B_Min', control_window, lower_green[2], 255, nothing)

    cv2.createTrackbar('R_Max', control_window, upper_green[0], 255, nothing)
    cv2.createTrackbar('G_Max', control_window, upper_green[1], 255, nothing)
    cv2.createTrackbar('B_Max', control_window, upper_green[2], 255, nothing)

    # Set up video capture
    vc_bg = None

    if constants.USE_TEST_FG_VIDEO:
        vc = cv2.VideoCapture(constants.TEST_FOREGROUND_VIDEO_PATH)
    else:
        vc = cv2.VideoCapture(0)

    frame = None
    test_foreground = cv2.imread(constants.TEST_FOREGROUND_IMAGE_PATH)
    test_background = cv2.imread(constants.TEST_BACKGROUND_IMAGE_PATH)
    if vc.isOpened():
        rval, frame = vc.read()

    if constants.USE_TEST_BG_VIDEO:
        vc_bg = cv2.VideoCapture(constants.TEST_BACKGROUND_VIDEO_PATH)

    # Main loop
    while vc.isOpened():

        # Get trackbar positions for RGB balance
        lower_green = np.array([cv2.getTrackbarPos('R_Min', control_window),
                       cv2.getTrackbarPos('G_Min', control_window),
                       cv2.getTrackbarPos('B_Min', control_window)])

        upper_green = np.array([cv2.getTrackbarPos('R_Max', control_window),
                       cv2.getTrackbarPos('G_Max', control_window),
                       cv2.getTrackbarPos('B_Max', control_window)])

        # Set up input images
        if constants.USE_TEST_FG_IMAGE:
            foreground_array = np.array(test_foreground)
        else:
            if constants.RESIZE_VIDEO:
                frame = cv2.resize(frame, constants.RESIZE_VIDEO)
            foreground_array = frame

        image_stats = Image.fromarray(foreground_array)
        signal_width = image_stats.width
        signal_height = image_stats.height


        if constants.USE_TEST_BG_IMAGE:
            background_array = np.array(test_background)
        elif constants.USE_TEST_BG_VIDEO:
            bg_rval, background_array = vc_bg.read()

            # If the background video ends, restart it
            # TODO: Fix this shit. It doesn't work
            if not vc_bg.isOpened():
                vc_bg = cv2.VideoCapture(constants.TEST_BACKGROUND_VIDEO_PATH)
        else:
            background_array = np.array(
                capture_background(
                    (constants.BG_X_OFFSET,
                     constants.BG_Y_OFFSET,
                     image_stats.width + constants.BG_X_OFFSET,
                     image_stats.height + constants.BG_Y_OFFSET)
                )
            )


        # Send images to chroma key method
        new_frame = green_screen(foreground_array, background_array)

        # Update GUI image, repeat until Escape key is pressed
        cv2.imshow("preview", new_frame)
        rval, frame = vc.read()
        cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)
        key = cv2.waitKey(20)
        if key == 27:
            break

    # Cleanup
    vc.release()
    cv2.destroyWindow("preview")


if __name__ == '__main__':
    main()

