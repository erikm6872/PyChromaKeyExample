import cv2
import numpy as np
import pyscreenshot as ImageGrab
from PIL import Image

import constants


def capture_background(bounds):
    """Captures a portion of the computer screen"""
    im = ImageGrab.grab(bbox=bounds)
    return im


class MaskedImage:
    def __init__(self, mask, image):
        self.mask = mask
        self.image = image


class GreenScreen:
    def __init__(self, video_size):
        self.signal_width, self.signal_height = video_size

    def process_foreground_image(self, frame, lower_green, upper_green):
        img = np.copy(frame)

        # Create an image mask to change green pixels to black
        mask = cv2.inRange(img, lower_green, upper_green)

        masked_image = np.copy(img)
        masked_image[mask != 0] = [0, 0, 0]

        return MaskedImage(mask, masked_image)

    def process_background_image(self, background_frame, mask):
        # Create another image mask to turn non-green pixels black on the background image
        try:
            background_image = cv2.cvtColor(background_frame, cv2.COLOR_BGR2RGB)
        except cv2.error as c:
            # This error occurs when the background video ends and does not restart.
            # TODO: FIX THIS BUG
            print("CV2 Error: " + repr(c))
            background_image = cv2.imread(constants.BACKGROUND_VIDEO_ERROR_PATH)
            masked_image = cv2.imread(constants.BACKGROUND_VIDEO_ERROR_PATH)
            masked_image = cv2.resize(masked_image, (self.signal_width, self.signal_height))

        crop_background = None
        try:
            crop_background = cv2.resize(background_image,
                                         (self.signal_width,
                                          self.signal_height))  # background_image[0:signal_height, 0:signal_width]
            crop_background[mask == 0] = [0, 0, 0]
        except cv2.error:
            # Debugging. `background_image` is null when bg video ends. If this happens, print error message and crash.
            print("image=" + repr(background_image) + " width=" + repr(self.signal_width) + " height=" + repr(self.signal_height))
            exit(0)
        return crop_background

    def chroma_key_image(self, frame, background_image, lower_green, upper_green, signal_width, signal_height):
        """Chroma key method."""
        cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)
        foreground = self.process_foreground_image(frame, lower_green, upper_green)
        background = self.process_background_image(background_image, foreground.mask)

        return np.array(foreground.image + background)

    def manual_pixel_replace(self, frame, background_image, lower_green, upper_green, signal_width, signal_height):
        fg_img = Image.fromarray(frame)
        bg_img = Image.fromarray(background_image)
