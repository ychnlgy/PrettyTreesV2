import math
from dataclasses import dataclass

from .geometry import Point
from .sprite_factory import BranchSpriteFactory
from .utils import cosineInterpolate, randDecay, randVariance


@dataclass(frozen=True, kw_only=True)
class BranchState:
    angle: float
    length: float
    width: float


@dataclass(frozen=True, kw_only=True)
class OffspringConfig:
    numChildren: int
    minThickness: float
    minLength: float
    fractionalFoodIntake: float

    # random variation
    thicknessDecayRange: tuple[float, float]
    lengthDecayRange: tuple[float, float]
    angleVariance: float
    depthVariance: float


class Branch:
    def __init__(
        self,
        spriteFactory: BranchSpriteFactory,
        position: Point,
        startState: BranchState,
        endState: BranchState,
    ) -> None:
        super().__init__()
        self._spriteFactory = spriteFactory
        self._position = position
        self._startState = startState
        self._endState = endState

        self._sprite = self._spriteFactory.create(position)
        self._currentState = startState
        self._updateSpriteState()

        self._progress = 0.0
        self._offspring: list[Branch] = []

    def grow(self, food: float, offspringConfig: OffspringConfig) -> None:
        foodToConsume, foodForOffspring = self._computeFoodIntake(food, offspringConfig)
        self._capProgress(foodToConsume)

        self._currentState = BranchState(
            angle=cosineInterpolate(
                self._startState.angle, self._endState.angle, self._progress
            ),
            length=cosineInterpolate(
                self._startState.length, self._endState.length, self._progress
            ),
            width=cosineInterpolate(
                self._startState.width, self._endState.width, self._progress
            ),
        )
        self._updateSpriteState()

        if foodForOffspring:
            self._feedOffspring(foodForOffspring, offspringConfig)
        else:
            self._attemptSpawnOffspring(offspringConfig)

    def setPosition(self, position: Point) -> None:
        self._position = position
        self._sprite.x = position.x
        self._sprite.y = position.y

    # === PRIVATE ===

    def _capProgress(self, food: float) -> None:
        self._progress = min(self._progress + food, 1.0)

    def _updateSpriteState(self) -> None:
        self._sprite.rotation = self._currentState.angle / 180.0 * math.pi
        spriteWidth, spriteHeight = self._spriteFactory.getDimensions()
        self._sprite.scale_x = self._currentState.length / spriteWidth
        # NOTE: the height of the sprite is actually the width of the branch
        self._sprite.scale_y = self._currentState.width / spriteHeight

    def _computeFoodIntake(
        self, food: float, offspringConfig: OffspringConfig
    ) -> tuple[float, float]:
        if not self._offspring:
            return food, 0.0
        foodToConsume = min(
            food * (1.0 - offspringConfig.fractionalFoodIntake), 1.0 - self._progress
        )
        foodForOffspring = food - foodToConsume
        return foodToConsume, foodForOffspring

    def _feedOffspring(self, food: float, offspringConfig: OffspringConfig) -> None:
        n = len(self._offspring)
        terminalPosition = self._computeTerminalPosition()
        for child in self._offspring:
            child.setPosition(terminalPosition)
            child.grow(food / n, offspringConfig)

    def _attemptSpawnOffspring(self, offspringConfig: OffspringConfig) -> None:
        if (
            self._currentState.length >= offspringConfig.minLength
            and self._currentState.width >= offspringConfig.minThickness
        ):
            for _ in range(offspringConfig.numChildren):
                startState = self._sampleStartState(offspringConfig)
                endState = self._sampleEndState(offspringConfig)
                position = self._computeTerminalPosition()
                child = Branch(self._spriteFactory, position, startState, endState)
                self._offspring.append(child)

    def _sampleStartState(self, offspringConfig: OffspringConfig) -> BranchState:
        """Samples a start state for an offspring branch based on the current state."""
        angle = randVariance(self._currentState.angle, offspringConfig.angleVariance)
        return BranchState(angle=angle, length=0.0, width=0.0)

    def _sampleEndState(self, offspringConfig: OffspringConfig) -> BranchState:
        """Samples an end state for an offspring branch based on the end state."""
        angle = randVariance(self._endState.angle, offspringConfig.angleVariance)
        length = randDecay(self._endState.length, offspringConfig.lengthDecayRange)
        width = randDecay(self._endState.width, offspringConfig.thicknessDecayRange)
        return BranchState(angle=angle, length=length, width=width)

    def _computeTerminalPosition(self) -> Point:
        angleRad = -self._currentState.angle / 180.0 * math.pi
        dx = math.cos(angleRad) * self._currentState.length
        dy = math.sin(angleRad) * self._currentState.length
        return Point(x=self._position.x + dx, y=self._position.y + dy)
