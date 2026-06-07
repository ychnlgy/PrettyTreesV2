import pathlib

import pyglet

from .branch import Branch, BranchState, OffspringConfig
from .branch_texture import SolidColorBranchTexture
from .color import Color
from .config import BranchCurvatureConfig, Config
from .curvature import computeCurvatureCircle
from .geometry import Point
from .sprite_factory import BranchSpriteFactory
from .utils import readFile

CURRENT_DIRECTORY = pathlib.Path(__file__).parent
SHADER_DIRECTORY = CURRENT_DIRECTORY / "shaders"
BRANCH_VERTEX_SHADER_PATH = SHADER_DIRECTORY / "branch_vertex.glsl"
BRANCH_FRAGMENT_SHADER_PATH = SHADER_DIRECTORY / "branch_fragment.glsl"


def main(config: Config) -> None:
    window = pyglet.window.Window(1200, 800, caption="Pretty Trees")
    batch = pyglet.graphics.Batch()

    vertShader = readFile(BRANCH_VERTEX_SHADER_PATH)
    fragShader = readFile(BRANCH_FRAGMENT_SHADER_PATH)
    shaderProgram = pyglet.graphics.shader.ShaderProgram(
        pyglet.graphics.shader.Shader(vertShader, "vertex"),
        pyglet.graphics.shader.Shader(fragShader, "fragment"),
    )

    branchTexture = SolidColorBranchTexture(Color(r=0, g=120, b=180))
    spriteFactory = BranchSpriteFactory(
        batch=batch, shaderProgram=shaderProgram, branchTexture=branchTexture
    )
    root = Branch(
        spriteFactory=spriteFactory,
        position=Point(x=600, y=100),
        startState=config.startBranchState,
        endState=config.endBranchState,
    )

    curvature = computeCurvatureCircle(
        midThickness=config.branchCurvature.midThickness,
        endThickness=config.branchCurvature.endThickness,
    )
    with shaderProgram:
        shaderProgram["branch_curvature_origin"] = curvature.origin.asTuple()
        shaderProgram["branch_curvature_radius"] = curvature.radius

    @window.event
    def on_draw() -> None:
        window.clear()
        batch.draw()

    def update(dt: float) -> None:
        root.grow(food=dt * 2.0, offspringConfig=config.offspringConfig)

    pyglet.clock.schedule_interval(update, 1 / 60)
    pyglet.app.run()


if __name__ == "__main__":
    config = Config(
        branchCurvature=BranchCurvatureConfig(
            midThickness=0.65,
            endThickness=0.80,
        ),
        startBranchState=BranchState(angle=-90.0, length=0.0, width=0.0),
        endBranchState=BranchState(angle=-90.0, length=100.0, width=20.0),
        offspringConfig=OffspringConfig(
            numChildren=2,
            minThickness=1,
            minLength=10,
            fractionalFoodIntake=0.5,
            # variation parameters
            thicknessDecayRange=(0.6, 0.75),
            lengthDecayRange=(0.8, 0.95),
            angleVariance=30.0,
            depthVariance=0.15,
        ),
    )
    main(config)
