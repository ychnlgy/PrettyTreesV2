import pathlib

import pyglet

from .branch_texture import SolidColorBranchTexture
from .color import Color
from .config import BranchCurvatureConfig, Config
from .curvature import computeCurvatureCircle
from .geometry import Point
from .utils import readFile

CURRENT_DIRECTORY = pathlib.Path(__file__).parent
SHADER_DIRECTORY = CURRENT_DIRECTORY / "shaders"
BRANCH_VERTEX_SHADER_PATH = SHADER_DIRECTORY / "branch_vertex.glsl"
BRANCH_FRAGMENT_SHADER_PATH = SHADER_DIRECTORY / "branch_fragment.glsl"


def main(config: Config) -> None:
    window = pyglet.window.Window(800, 600, caption="Pretty Trees")
    batch = pyglet.graphics.Batch()

    vertShader = readFile(BRANCH_VERTEX_SHADER_PATH)
    fragShader = readFile(BRANCH_FRAGMENT_SHADER_PATH)
    shaderProgram = pyglet.graphics.shader.ShaderProgram(
        pyglet.graphics.shader.Shader(vertShader, "vertex"),
        pyglet.graphics.shader.Shader(fragShader, "fragment"),
    )

    branchTexture = SolidColorBranchTexture(Color(r=0, g=120, b=180))
    branchTexture.createSprite(
        Point(x=400, y=300),
        batch,
        shaderProgram,
    )

    computeCurvatureCircle(
        midThickness=config.branchCurvature.midThickness,
        endThickness=config.branchCurvature.endThickness,
    )
    # with shaderProgram:
    #     shaderProgram["branch_curvature_origin"] = curvature.origin.asTuple()
    #     shaderProgram["branch_curvature_radius"] = curvature.radius

    @window.event
    def on_draw() -> None:
        window.clear()
        batch.draw()

    def update(dt: float) -> None:
        pass

    pyglet.clock.schedule_interval(update, 1 / 60)
    pyglet.app.run()


if __name__ == "__main__":
    config = Config(
        branchCurvature=BranchCurvatureConfig(
            midThickness=0.65,
            endThickness=0.80,
        )
    )
    main(config)
