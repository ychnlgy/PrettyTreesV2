from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class BranchCurvatureConfig:
    midThickness: float
    endThickness: float


@dataclass(frozen=True, kw_only=True)
class Config:
    branchCurvature: BranchCurvatureConfig
