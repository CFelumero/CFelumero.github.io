"""
Minimal shim of the parts of the `arcade` library this project uses.
This is the ONLY new code involved in the port. froggerFunctions.py,
froggerHelper.py, and main.py are the student's original, unmodified
files -- this module exists purely so those files have an `arcade` to
import, with actual drawing/sound calls forwarded to JavaScript since
a browser can't open a native OpenGL window the way desktop Python can.
"""
import js as _js


class _Color:
    DARK_SPRING_GREEN = (23, 105, 54)
    GRAY = (128, 128, 128)
    YELLOW = (255, 220, 0)
    WHITE = (255, 255, 255)
    RED = (200, 40, 40)
    PURPLE_HEART = (105, 53, 201)
    BLACK = (0, 0, 0)


color = _Color()


class _Key:
    UP = "ArrowUp"
    DOWN = "ArrowDown"
    LEFT = "ArrowLeft"
    RIGHT = "ArrowRight"
    W = "w"
    A = "a"
    S = "s"
    D = "d"
    MOTION_END_OF_FILE = object()


key = _Key()

_current_window = None


class Texture:
    def __init__(self, image_key, flipped_horizontally=False):
        self.image_key = image_key
        self.flipped_horizontally = flipped_horizontally


def load_texture(path, flipped_horizontally=False):
    return Texture(path, flipped_horizontally)


class Sound:
    def __init__(self, path):
        self.path = path


def load_sound(path):
    return Sound(path)


def play_sound(sound):
    if sound is not None:
        _js._playSound(sound.path)


class Sprite:
    def __init__(self, filename=None):
        self._filename = filename
        self.center_x = 0.0
        self.center_y = 0.0
        self.angle = 0
        self._scale = 1.0
        self.texture = None
        self.textures = []
        if filename:
            w, h = _js._getImageSize(filename)
            self._nat_w = w
            self._nat_h = h
        else:
            self._nat_w = 64
            self._nat_h = 64

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value

    @property
    def width(self):
        return self._nat_w * self._scale

    @property
    def height(self):
        return self._nat_h * self._scale

    def collides_with_sprite(self, other):
        return check_for_collision(self, other)

    def draw(self):
        if self.texture is not None:
            image_key = self.texture.image_key
            flipped = self.texture.flipped_horizontally
        else:
            image_key = self._filename
            flipped = False
        _js._drawSprite(image_key, self.center_x, self.center_y,
                          self.width, self.height, self.angle, flipped)


class SpriteList(list):
    def draw(self):
        for sprite in self:
            sprite.draw()


def _overlap(a, b):
    return (abs(a.center_x - b.center_x) * 2 < (a.width + b.width) and
            abs(a.center_y - b.center_y) * 2 < (a.height + b.height))


def check_for_collision(a, b):
    return _overlap(a, b)


def check_for_collision_with_list(sprite, sprite_list):
    for other in sprite_list:
        if check_for_collision(sprite, other):
            return True
    return False


def draw_xywh_rectangle_filled(x, y, w, h, color_value):
    r, g, b = color_value
    _js._drawRect(x, y, w, h, r, g, b)


class Text:
    def __init__(self, text, x, y, color_value=None, font_size=12, width=None,
                 anchor_x="left", **kwargs):
        self.text = text
        self.x = x
        self.y = y
        self.color = color_value if color_value is not None else _Color.WHITE
        self.font_size = font_size
        self.anchor_x = anchor_x

    def draw(self):
        r, g, b = self.color
        _js._drawText(self.text, self.x, self.y, r, g, b, self.font_size, self.anchor_x)


def start_render():
    pass


def finish_render():
    pass


class Window:
    def __init__(self, width, height, title=""):
        global _current_window
        self.width = width
        self.height = height
        self.title = title
        _current_window = self


def run():
    # The real event loop lives in JavaScript (requestAnimationFrame);
    # it calls on_update / on_draw / on_key_press on _current_window directly.
    pass
