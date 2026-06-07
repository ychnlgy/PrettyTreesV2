import abc

import pyglet

from .color import Color
from .geometry import Point

DEFAULT_WIDTH = 10
DEFAULT_HEIGHT = 10


class BranchTextureInterface(abc.ABC):
    @abc.abstractmethod
    def createSprite(
        self,
        position: Point,
        batch: pyglet.graphics.Batch,
        program: pyglet.graphics.shader.ShaderProgram,
    ) -> pyglet.sprite.Sprite:
        """Creates a pyglet sprite."""

    @abc.abstractmethod
    def getDimensions(self) -> tuple[float, float]:
        """Returns the dimensions of the sprite as (width, height)."""


class SolidColorBranchTexture(BranchTextureInterface):
    def __init__(self, color: Color) -> None:
        super().__init__()
        pattern = pyglet.image.SolidColorImagePattern(color.asTuple())
        self._image = pattern.create_image(DEFAULT_WIDTH, DEFAULT_HEIGHT)
        self._image.anchor_y = DEFAULT_HEIGHT // 2

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

    def getDimensions(self) -> tuple[float, float]:
        return self._image.width, self._image.height
