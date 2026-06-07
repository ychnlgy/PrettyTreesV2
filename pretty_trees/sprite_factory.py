import abc

import pyglet

from .branch_texture import BranchTextureInterface
from .geometry import Point


class SpriteFactoryInterface(abc.ABC):
    @abc.abstractmethod
    def create(self, position: Point) -> pyglet.sprite.Sprite:
        """Creates a pyglet sprite."""

    @abc.abstractmethod
    def getDimensions(self) -> tuple[float, float]:
        """Returns the dimensions of the sprite as (width, height)."""


class BranchSpriteFactory(SpriteFactoryInterface):
    def __init__(
        self,
        batch: pyglet.graphics.Batch,
        shaderProgram: pyglet.graphics.shader.ShaderProgram,
        branchTexture: BranchTextureInterface,
    ) -> None:
        self._batch = batch
        self._shaderProgram = shaderProgram
        self._branchTexture = branchTexture

    def create(self, position: Point) -> pyglet.sprite.Sprite:
        return self._branchTexture.createSprite(
            position=position,
            batch=self._batch,
            program=self._shaderProgram,
        )

    def getDimensions(self) -> tuple[float, float]:
        return self._branchTexture.getDimensions()
