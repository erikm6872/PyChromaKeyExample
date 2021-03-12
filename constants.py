LOWER_GREEN = ([0, 100, 0])
UPPER_GREEN = ([80, 255, 40])

USE_TEST_FG_IMAGE = True
USE_TEST_BG_IMAGE = True    # Using the test background image reduces lag significantly
USE_TEST_FG_VIDEO = False
USE_TEST_BG_VIDEO = False   # Background videos are currently bugged. TODO: FIX

TEST_FOREGROUND_IMAGE_PATH = 'res/green_test.png'
TEST_BACKGROUND_IMAGE_PATH = 'res/background_image.jpg'
TEST_FOREGROUND_VIDEO_PATH = 'res/sample_greenscreen_video.mp4'
TEST_BACKGROUND_VIDEO_PATH = 'res/space.mp4'
BACKGROUND_VIDEO_ERROR_PATH = 'res/background_error.png'

BG_X_OFFSET = 10
BG_Y_OFFSET = 10


RESIZE_VIDEO = (800, 600)    # Set to 0 to keep original size. High-res videos can cause significant lag.

SHOW_PREVIEW = True

# Web server configs
STREAM_HTTP = True
HTTP_PORT = 1738
