import pyglet

from .branch import Branch, BranchState, OffspringConfig
from .branch_texture import ImageBranchTexture
from .config import BranchCurvatureConfig, Config
from .constants import (
    BRANCH_FRAGMENT_SHADER_PATH,
    BRANCH_VERTEX_SHADER_PATH,
    SCRIBBLE_TEXTURE_PATH,
    TREE_X,
    TREE_Y,
)
from .curvature import computeCurvatureCircle
from .geometry import Point
from .scene import AggregateScene, BasicTexturedScene, RedSunScene
from .sprite_factory import BranchSpriteFactory
from .utils import readFile


def main(config: Config) -> None:
    windowSize = Point(x=1200, y=900)
    window = pyglet.window.Window(
        int(windowSize.x), int(windowSize.y), caption="Pretty Trees"
    )
    batch = pyglet.graphics.Batch()

    vertShader = readFile(BRANCH_VERTEX_SHADER_PATH)
    fragShader = readFile(BRANCH_FRAGMENT_SHADER_PATH)
    shaderProgram = pyglet.graphics.shader.ShaderProgram(
        pyglet.graphics.shader.Shader(vertShader, "vertex"),
        pyglet.graphics.shader.Shader(fragShader, "fragment"),
    )

    # branchTexture = SolidColorBranchTexture(Color(r=0, g=120, b=180))
    branchTexture = ImageBranchTexture(SCRIBBLE_TEXTURE_PATH)
    spriteFactory = BranchSpriteFactory(
        batch=batch, shaderProgram=shaderProgram, branchTexture=branchTexture
    )
    root = Branch(
        spriteFactory=spriteFactory,
        position=Point(x=TREE_X, y=TREE_Y),
        startState=config.startBranchState,
        endState=config.endBranchState,
    )

    scene = AggregateScene()
    scene.addScene(
        BasicTexturedScene(
            lifeTime=0.1,
            root=root,
            config=config,
        )
    )
    scene.addScene(
        RedSunScene(
            lifeTime=10.0,
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

    # bufferPattern = pyglet.image.SolidColorImagePattern(color=(0, 0, 0, 0))
    # buffer = bufferPattern.create_image(int(windowSize.x), int(windowSize.y)).get_texture()

    buffer = pyglet.image.create(int(windowSize.x), int(windowSize.y) - TREE_Y)
    bufferTex = buffer.get_texture()

    @window.event
    def on_draw() -> None:
        window.clear()
        scene.predraw()
        batch.draw()
        screenshot = (
            pyglet.image.get_buffer_manager()
            .get_color_buffer()
            .get_region(0, TREE_Y, int(windowSize.x), int(windowSize.y) - TREE_Y)
        )
        bufferTex.blit_into(screenshot, 0, 0, 0)
        scene.postdraw(buffer)

    def update(dt: float) -> None:
        scene.update(dt)

    pyglet.clock.schedule_interval(update, 1 / 60)
    pyglet.app.run()


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
            # variation parameters
            thicknessDecayRange=(0.7, 0.85),
            lengthDecayRange=(0.8, 0.95),
            angleVariance=30.0,
            depthVariance=0.15,
        ),
        depthEffectMultiplier=0.0,
        growthSpeed=2.0,
    )
    main(config)
