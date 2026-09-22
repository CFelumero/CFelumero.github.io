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

    def _current_image_key(self):
        # Sprites like Player set .texture after construction (with no
        # filename passed to __init__), so size/hitbox must be resolved
        # from whichever texture is actually active right now, not
        # cached from construction time.
        if self.texture is not None:
            return self.texture.image_key
        return self._filename

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value

    @property
    def width(self):
        key = self._current_image_key()
        if not key:
            return 64 * self._scale
        w, h = _js._getImageSize(key)
        return w * self._scale

    @property
    def height(self):
        key = self._current_image_key()
        if not key:
            return 64 * self._scale
        w, h = _js._getImageSize(key)
        return h * self._scale

    @property
    def hb_width(self):
        # Collision size: cropped to the sprite's actual non-transparent
        # pixels, matching arcade's default "Simple" hit box algorithm,
        # rather than the full (possibly padded) image bounds.
        key = self._current_image_key()
        if not key:
            return 64 * self._scale
        hb_w, hb_h, dx, dy = _js._getHitbox(key)
        return hb_w * self._scale

    @property
    def hb_height(self):
        key = self._current_image_key()
        if not key:
            return 64 * self._scale
        hb_w, hb_h, dx, dy = _js._getHitbox(key)
        return hb_h * self._scale

    @property
    def hb_center_x(self):
        key = self._current_image_key()
        if not key:
            return self.center_x
        hb_w, hb_h, dx, dy = _js._getHitbox(key)
        return self.center_x + dx * self._scale

    @property
    def hb_center_y(self):
        key = self._current_image_key()
        if not key:
            return self.center_y
        hb_w, hb_h, dx, dy = _js._getHitbox(key)
        return self.center_y + dy * self._scale

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
    return (abs(a.hb_center_x - b.hb_center_x) * 2 < (a.hb_width + b.hb_width) and
            abs(a.hb_center_y - b.hb_center_y) * 2 < (a.hb_height + b.hb_height))


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


def draw_text(text, start_x, start_y, color_value=None, font_size=12, anchor_x="left", **kwargs):
    r, g, b = color_value if color_value is not None else _Color.WHITE
    _js._drawText(text, start_x, start_y, r, g, b, font_size, anchor_x)


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
