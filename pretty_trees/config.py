from dataclasses import dataclass

from .branch import BranchState, OffspringConfig


@dataclass(frozen=True, kw_only=True)
class BranchCurvatureConfig:
    midThickness: float
    endThickness: float


@dataclass(frozen=True, kw_only=True)
class Config:
    branchCurvature: BranchCurvatureConfig

    startBranchState: BranchState
    endBranchState: BranchState
    offspringConfig: OffspringConfig

    depthEffectMultiplier: float
