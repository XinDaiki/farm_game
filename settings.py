# Game Settings
TILE_SIZE = 32
MAP_WIDTH = 30
MAP_HEIGHT = 17
DEFAULT_SCREEN_WIDTH = TILE_SIZE * MAP_WIDTH
DEFAULT_SCREEN_HEIGHT = TILE_SIZE * MAP_HEIGHT
MIN_SCREEN_WIDTH = 800
MIN_SCREEN_HEIGHT = 600
FPS = 60

# Dynamic screen size (will be updated by game)
SCREEN_WIDTH = DEFAULT_SCREEN_WIDTH
SCREEN_HEIGHT = DEFAULT_SCREEN_HEIGHT

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
BLUE = (64, 164, 223)
DARK_GREEN = (20, 80, 20)
LIGHT_BROWN = (210, 180, 140)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 100)
RED = (200, 50, 50)

# Game Balance
INITIAL_SEEDS = 10
INITIAL_MONEY = 100
CROP_SELL_MULTIPLIER = 2

# Time Settings
TIME_SPEED = 0.001  # How fast time passes
NIGHT_START = 18
NIGHT_END = 6

def update_screen_size(width, height):
    """Update global screen size variables"""
    global SCREEN_WIDTH, SCREEN_HEIGHT
    SCREEN_WIDTH = max(MIN_SCREEN_WIDTH, width)
    SCREEN_HEIGHT = max(MIN_SCREEN_HEIGHT, height)