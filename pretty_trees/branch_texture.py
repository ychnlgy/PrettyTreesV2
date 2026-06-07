import abc

import pyglet

from .color import Color
from .geometry import Point

DEFAULT_WIDTH = 100
DEFAULT_HEIGHT = 50


class BranchTextureInterface(abc.ABC):
    @abc.abstractmethod
    def createSprite(
        self,
        position: Point,
        batch: pyglet.graphics.Batch,
        program: pyglet.graphics.shader.ShaderProgram,
    ) -> pyglet.sprite.Sprite:
        """Creates a pyglet sprite."""


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
