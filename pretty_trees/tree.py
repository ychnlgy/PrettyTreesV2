import pyglet

from .branch_texture import BranchTextureInterface
from .geometry import Point


class Tree:
    def __init__(
        self,
        batch: pyglet.graphics.Batch,
        shaderProgram: pyglet.graphics.shader.ShaderProgram,
        branchTexture: BranchTextureInterface,
    ) -> None:
        self._batch = batch
        self._shaderProgram = shaderProgram
        self._branchTexture = branchTexture
        self._sprites: list[pyglet.sprite.Sprite] = []

    def addBranch(self, position: Point) -> None:
        sprite = self._branchTexture.createSprite(
            position=position,
            batch=self._batch,
            program=self._shaderProgram,
        )
        self._sprites.append(sprite)

    def update(self, dt: float) -> None:
        for sprite in self._sprites:
            sprite.rotation += dt * 5
