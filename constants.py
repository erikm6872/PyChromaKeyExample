LOWER_GREEN = ([0, 100, 0])
UPPER_GREEN = ([130, 255, 83])

USE_TEST_FG_IMAGE = False
USE_TEST_BG_IMAGE = False    # Using the test background image reduces lag significantly
USE_TEST_FG_VIDEO = True
USE_TEST_BG_VIDEO = True   # Background videos are currently bugged. TODO: FIX

#  Stock Footage by <a href="http://www.videezy.com">Videezy.com</a>
TEST_FOREGROUND_IMAGE_PATH = 'res/green_test.png'
TEST_BACKGROUND_IMAGE_PATH = 'res/background_image.jpg'
TEST_FOREGROUND_VIDEO_PATH = 'res/sample_greenscreen_video.mp4'
TEST_BACKGROUND_VIDEO_PATH = 'res/space.mp4'
BACKGROUND_VIDEO_ERROR_PATH = 'res/background_error.png'

BG_X_OFFSET = 10
BG_Y_OFFSET = 10

# Set to 0 to keep original size. format: (height, width), eg (800, 600) High-res videos can cause significant lag.
RESIZE_VIDEO = 0

SHOW_PREVIEW = True

# Web server configs
STREAM_HTTP = True
HTTP_PORT = 1738
