import random

import cv2
import numpy
import pyglet

from .branch import Branch, BranchState, OffspringConfig
from .branch_texture import ImageBranchTexture
from .config import BranchCurvatureConfig, Config
from .constants import (
    BRANCH_FRAGMENT_SHADER_PATH,
    BRANCH_VERTEX_SHADER_PATH,
    SCRIBBLE_TEXTURE_PATH,
    TREE_Y,
)
from .curvature import computeCurvatureCircle
from .geometry import Point
from .scene import (
    AggregateScene,
    BasicTexturedScene,
    GalaxyScene,
    RedSunScene,
    SnowScene,
)
from .sprite_factory import BranchSpriteFactory
from .utils import readFile


def makeWindow(recording: bool) -> pyglet.window.Window:
    title = "Pretty Trees"
    if recording:
        return pyglet.window.Window(1920, 1080, caption=title, visible=False)
    else:
        return pyglet.window.Window(fullscreen=True, caption=title)


def main(config: Config) -> None:
    cv2Recording = False
    random.seed(1337)
    window = makeWindow(cv2Recording)
    windowSize = Point(x=window.width, y=window.height)
    batch = pyglet.graphics.Batch()

    vertShader = readFile(BRANCH_VERTEX_SHADER_PATH)
    fragShader = readFile(BRANCH_FRAGMENT_SHADER_PATH)
    shaderProgram = pyglet.graphics.shader.ShaderProgram(
        pyglet.graphics.shader.Shader(vertShader, "vertex"),
        pyglet.graphics.shader.Shader(fragShader, "fragment"),
    )

    branchTexture = ImageBranchTexture(SCRIBBLE_TEXTURE_PATH)
    spriteFactory = BranchSpriteFactory(
        batch=batch, shaderProgram=shaderProgram, branchTexture=branchTexture
    )
    root = Branch(
        spriteFactory=spriteFactory,
        position=Point(x=windowSize.x // 2, y=TREE_Y),
        startState=config.startBranchState,
        endState=config.endBranchState,
    )

    scene = AggregateScene()
    scene.addScene(
        BasicTexturedScene(
            lifeTime=6.0,
            root=root,
            config=config,
        )
    )
    scene.addScene(
        RedSunScene(
            lifeTime=16.0,
            root=root,
            config=config,
            windowSize=windowSize,
        )
    )
    scene.addScene(
        GalaxyScene(
            lifeTime=46.0,
            root=root,
            config=config,
            windowSize=windowSize,
        )
    )

    scene.addScene(
        SnowScene(
            lifeTime=25.0,
            root=root,
            config=config,
            windowSize=windowSize,
        )
    )

    curvature = computeCurvatureCircle(
        midThickness=config.branchCurvature.midThickness,
        endThickness=config.branchCurvature.endThickness,
    )
    with shaderProgram:
        shaderProgram["branch_curvature_origin"] = curvature.origin.asTuple()
        shaderProgram["branch_curvature_radius"] = curvature.radius
        shaderProgram["depth_effect_multiplier"] = config.depthEffectMultiplier

    buffer = pyglet.image.create(int(windowSize.x), int(windowSize.y) - TREE_Y)
    bufferTex = buffer.get_texture()

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # ty: ignore[unresolved-attribute]
    fps = 30.0
    width, height = int(windowSize.x), int(windowSize.y)
    videoWriter = cv2.VideoWriter("output.mp4", fourcc, fps, (width, height))

    scene.initialize()

    def drawUpdate() -> None:
        window.clear()
        scene.predraw()
        if not scene.skipTreeDrawing():
            batch.draw()
        screenshot = (
            pyglet.image.get_buffer_manager()
            .get_color_buffer()
            .get_region(0, TREE_Y, int(windowSize.x), int(windowSize.y) - TREE_Y)
        )
        bufferTex.blit_into(screenshot, 0, 0, 0)
        scene.postdraw(buffer)

    @window.event
    def on_draw() -> None:
        drawUpdate()

    def screenRecord() -> None:
        drawUpdate()

        # Convert the buffer to a format suitable for OpenCV
        imageData = (
            pyglet.image.get_buffer_manager().get_color_buffer().get_image_data()
        )
        data = imageData.get_data("RGB", imageData.width * 3)
        frame = numpy.frombuffer(data, dtype=numpy.uint8).reshape(
            imageData.height, imageData.width, 3
        )
        frameBgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        videoWriter.write(cv2.flip(frameBgr, 0))

    def update(dt: float) -> None:
        delta = 1 / fps if cv2Recording else dt
        scene.update(delta)
        if cv2Recording:
            screenRecord()

    pyglet.clock.schedule_interval(update, 1 / 60)
    try:
        pyglet.app.run()
    finally:
        videoWriter.release()


if __name__ == "__main__":
    config = Config(
        branchCurvature=BranchCurvatureConfig(
            midThickness=0.65,
            endThickness=0.80,
        ),
        startBranchState=BranchState(angle=-90.0, length=0.0, width=0.0, depth=0.0),
        endBranchState=BranchState(angle=-90.0, length=100.0, width=20.0, depth=0.0),
        offspringConfig=OffspringConfig(
            numChildren=2,
            minThickness=1.2,
            minLength=10.0,
            fractionalFoodIntake=0.5,
            malnutrition=0.95,
            # variation parameters
            thicknessDecayRange=(0.7, 0.85),
            lengthDecayRange=(0.8, 0.95),
            angleVariance=30.0,
            depthVariance=0.15,
        ),
        depthEffectMultiplier=0.0,
        growthSpeed=1.0,
    )
    main(config)
