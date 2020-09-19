import cv2
import numpy as np
from PIL import Image
import pyscreenshot as ImageGrab
from pychromakey import ChromaKey, ChromaKeyGUI

import constants


def capture_background(bounds):
    """Captures a portion of the computer screen"""
    im = ImageGrab.grab(bbox=bounds)
    return im


def main():
    """Main program loop"""
    with ChromaKeyGUI.ChromaKeyGUI(constants.SHOW_PREVIEW) as gui:

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

            gui.update_values()

            # Set up input images
            if constants.USE_TEST_FG_IMAGE:
                foreground_array = np.array(test_foreground)
            else:
                foreground_array = frame

            if constants.RESIZE_VIDEO:
                foreground_array = cv2.resize(foreground_array, constants.RESIZE_VIDEO)

            image_stats = Image.fromarray(foreground_array)
            gs = ChromaKey.ChromaKey((image_stats.width, image_stats.height))

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
            new_frame = gs.chroma_key_image(
                foreground_array,
                background_array,
                gui.lower_green,
                gui.upper_green)

            # Update GUI image, repeat until Escape key is pressed
            gui.update_preview(new_frame)

            rval, frame = vc.read()

            key = cv2.waitKey(20)
            if key == 27:
                break
        vc.release()


if __name__ == '__main__':
    main()

