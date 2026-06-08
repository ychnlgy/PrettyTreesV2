import abc
import math
from collections import deque

import pyglet

from .branch import Branch
from .branch_texture import SolidColorBranchTexture
from .color import Color
from .config import Config
from .constants import (
    GALAXY_TEXTURE_PATH,
    REFLECTION_FRAGMENT_SHADER_PATH,
    REFLECTION_VERTEX_SHADER_PATH,
    SHADOW_FRAGMENT_SHADER_PATH,
    SHADOW_VERTEX_SHADER_PATH,
    TREE_Y,
)
from .geometry import Point
from .utils import readFile


class SceneInterface(abc.ABC):
    @abc.abstractmethod
    def setGrowthDirection(self, growthDirection: float) -> None:
        """Sets the growth direction for the scene, where 1.0 is normal growth and negative values reverse growth."""

    @abc.abstractmethod
    def update(self, dt: float) -> bool:
        """Updates the scene by a given time delta, returning False if the scene concluded."""

    @abc.abstractmethod
    def initialize(self) -> None:
        """Called when the scene becomes active between scene transitions."""

    @abc.abstractmethod
    def predraw(self) -> None:
        """Called before drawing the scene."""

    @abc.abstractmethod
    def postdraw(self, buffer: pyglet.image.AbstractImage) -> None:
        """Called after drawing the scene."""


class AggregateScene(SceneInterface):
    def __init__(self) -> None:
        super().__init__()
        self._scenes: deque[SceneInterface] = deque()

    def addScene(self, scene: SceneInterface) -> None:
        self._scenes.append(scene)

    def setGrowthDirection(self, growthDirection: float) -> None:
        raise NotImplementedError

    def update(self, dt: float) -> bool:
        output = bool(self._scenes)
        if output:
            output = self._scenes[0].update(dt)
            if not output and len(self._scenes) > 1:
                self._scenes.popleft()
                self._scenes[0].initialize()
        return output

    def initialize(self) -> None:
        pass

    def predraw(self) -> None:
        if self._scenes:
            self._scenes[0].predraw()

    def postdraw(self, buffer: pyglet.image.AbstractImage) -> None:
        if self._scenes:
            self._scenes[0].postdraw(buffer)


class AbstractScene(SceneInterface):
    def __init__(
        self,
        lifeTime: float,
        root: Branch,
        config: Config,
    ) -> None:
        super().__init__()
        self._fullTime = lifeTime
        self._lifeTime = lifeTime
        self._root = root
        self._config = config
        self._growthDirection = 1.0

    def setGrowthDirection(self, growthDirection: float) -> None:
        self._growthDirection = growthDirection

    def update(self, dt: float) -> bool:
        self._root.grow(
            food=dt * self._config.growthSpeed * self._growthDirection,
            offspringConfig=self._config.offspringConfig,
        )
        self._lifeTime -= dt
        self.updateScene(progress=1.0 - max(0.0, self._lifeTime / self._fullTime))
        return self._lifeTime > 0.0

    def initialize(self) -> None:
        self.initializeTree(tree=self._root)

    # === PROTECTED ===

    @abc.abstractmethod
    def updateScene(self, progress: float) -> None:
        """Called during update with the current progress of the scene's lifetime (0.0 to 1.0)."""

    @abc.abstractmethod
    def initializeTree(self, tree: Branch) -> None:
        """Called during initialization with the tree root, allowing for scene-specific tree setup."""


class BasicTexturedScene(AbstractScene):
    def predraw(self) -> None:
        pass

    def postdraw(self, buffer: pyglet.image.AbstractImage) -> None:
        pass

    # === PROTECTED ===

    def updateScene(self, progress: float) -> None:
        pass

    def initializeTree(self, tree: Branch) -> None:
        pass


class RedSunScene(AbstractScene):
    def __init__(
        self,
        lifeTime: float,
        root: Branch,
        config: Config,
        windowSize: Point,
    ) -> None:
        super().__init__(lifeTime, root, config)
        self._windowSize = windowSize

        # parameters
        self._minSunX = windowSize.x * -0.1
        self._maxSunX = windowSize.x * 1.1
        self._minSunY = -windowSize.y * 0.75
        self._maxSunY = windowSize.y * 0.85

        self._minSunSky = windowSize.y * -0.25
        self._maxSunSky = windowSize.y * 0.25

        # sprites
        self._sun = pyglet.shapes.Circle(
            x=self._minSunX,
            y=self._minSunY,
            radius=50,
            color=(255, 0, 0),
        )
        self._sky = pyglet.shapes.Rectangle(
            x=0,
            y=0,
            width=windowSize.x,
            height=windowSize.y,
            color=(255, 255, 255, 0),
        )

        vertShader = readFile(SHADOW_VERTEX_SHADER_PATH)
        fragShader = readFile(SHADOW_FRAGMENT_SHADER_PATH)
        self._shadowShaderProgram = pyglet.graphics.shader.ShaderProgram(
            pyglet.graphics.shader.Shader(vertShader, "vertex"),
            pyglet.graphics.shader.Shader(fragShader, "fragment"),
        )

    def predraw(self) -> None:
        self._sky.draw()
        self._sun.draw()

    def postdraw(self, buffer: pyglet.image.AbstractImage) -> None:
        y = TREE_Y - buffer.height
        ground = pyglet.sprite.Sprite(
            buffer, x=0, y=y, program=self._shadowShaderProgram
        )

        with self._shadowShaderProgram:
            ground.draw()

    # === PROTECTED ===

    def updateScene(self, progress: float) -> None:
        yProgress = ((1 - math.cos(progress * 2 * math.pi)) / 2) ** 0.1
        sunX = self._minSunX + (self._maxSunX - self._minSunX) * progress
        sunY = self._minSunY + (self._maxSunY - self._minSunY) * yProgress

        skyAlpha = int(
            255
            * min(1.0, (sunY - self._minSunSky) / (self._maxSunSky - self._minSunSky))
        )

        self._sun.x = sunX
        self._sun.y = sunY
        self._sky.color = (255, 255, 255, skyAlpha)

        self._shadowShaderProgram["progress"] = progress
        self._shadowShaderProgram["progress_slope"] = 5.0

    def initializeTree(self, tree: Branch) -> None:
        pass


class GalaxyScene(AbstractScene):
    def __init__(
        self,
        lifeTime: float,
        root: Branch,
        config: Config,
        windowSize: Point,
    ) -> None:
        super().__init__(lifeTime, root, config)
        self._windowSize = windowSize
        self._treeRoot = root  # for manipulating colors

        # textures
        self._branchTexture = SolidColorBranchTexture(Color(r=0, g=0, b=0))

        # background
        self._backgroundImg = pyglet.image.load(GALAXY_TEXTURE_PATH.as_posix())
        scale = 1.2
        self._wiggleRoom = max(0, self._backgroundImg.width * scale - windowSize.x)
        self._backgroundSprite = pyglet.sprite.Sprite(
            self._backgroundImg,
            x=0,
            y=TREE_Y,
        )
        self._backgroundSprite.scale = scale

        # reflection
        vertShader = readFile(REFLECTION_VERTEX_SHADER_PATH)
        fragShader = readFile(REFLECTION_FRAGMENT_SHADER_PATH)
        self._reflectionShaderProgram = pyglet.graphics.shader.ShaderProgram(
            pyglet.graphics.shader.Shader(vertShader, "vertex"),
            pyglet.graphics.shader.Shader(fragShader, "fragment"),
        )

        self._isDying = False

    def predraw(self) -> None:
        self._backgroundSprite.draw()

    def postdraw(self, buffer: pyglet.image.AbstractImage) -> None:
        y = TREE_Y - buffer.height
        reflection = pyglet.sprite.Sprite(
            buffer, x=0, y=y, program=self._reflectionShaderProgram
        )
        with self._reflectionShaderProgram:
            reflection.draw()

    # === PROTECTED ===

    def updateScene(self, progress: float) -> None:
        cosineProgress = ((1 - math.cos(progress * math.pi)) / 2) ** 0.1
        self._backgroundSprite.opacity = int(255 * cosineProgress)
        self._backgroundSprite.x = -self._wiggleRoom * progress

        colorProgress = ((1 - math.cos(progress * 16 * math.pi)) / 2) ** 2
        value = int(255 * colorProgress)
        self._branchTexture = SolidColorBranchTexture(Color(r=value, g=value, b=value))
        self._treeRoot.propagateImage(self._branchTexture)
        self._reflectionShaderProgram["time"] = progress * 10.0

        if progress > 0.5 and not self._isDying:
            self._isDying = True
            self.setGrowthDirection(-0.4)

    def initializeTree(self, tree: Branch) -> None:
        tree.replaceImage(self._branchTexture)
