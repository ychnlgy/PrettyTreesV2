import pyglet

from .color import Color
from .geometry import Point

DEFAULT_WIDTH = 100
DEFAULT_HEIGHT = 50


class SolidColorBranchTexture:
    def __init__(self, color: Color) -> None:
        super().__init__()
        pattern = pyglet.image.SolidColorImagePattern(color.asTuple())
        self._image = pattern.create_image(DEFAULT_WIDTH, DEFAULT_HEIGHT)

    def createSprite(
        self,
        position: Point,
        batch: pyglet.graphics.Batch,
        program: pyglet.graphics.shader.ShaderProgram,
    ) -> pyglet.sprite.Sprite:
        return pyglet.sprite.Sprite(
            self._image,
            x=position.x,
            y=position.y,
            batch=batch,
            program=program,
        )
