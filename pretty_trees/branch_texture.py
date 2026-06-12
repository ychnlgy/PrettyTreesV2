import abc
import pathlib

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

    @abc.abstractmethod
    def getImage(self) -> pyglet.image.AbstractImage:
        """Returns the image used for the sprite."""


class AbstractBranchTexture(BranchTextureInterface):
    def __init__(self, image: pyglet.image.AbstractImage) -> None:
        super().__init__()
        image.anchor_y = image.height // 2
        self._image = image

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
            z=0.0,
            batch=batch,
            program=program,
        )

    def getDimensions(self) -> tuple[float, float]:
        return self._image.width, self._image.height

    def getImage(self) -> pyglet.image.AbstractImage:
        return self._image


class SolidColorBranchTexture(AbstractBranchTexture):
    def __init__(self, color: Color) -> None:
        pattern = pyglet.image.SolidColorImagePattern(color.asTuple())
        image = pattern.create_image(DEFAULT_WIDTH, DEFAULT_HEIGHT)
        super().__init__(image)


class ImageBranchTexture(AbstractBranchTexture):
    def __init__(self, imagePath: pathlib.Path) -> None:
        image = pyglet.image.load(imagePath.as_posix())
        super().__init__(image)
