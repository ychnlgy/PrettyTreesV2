# Contents
<pre>
classes
└── pretty_trees
    ├── geometry.py
    │   └── <a href='#circle'>Circle</a>
    └── config.py
        └── <a href='#config'>Config</a>
</pre>

### Circle
Back to [top](#contents).

```python
from pretty_trees.geometry import Circle
```

```python
@dataclass(frozen=True, kw_only=True)
class Circle:
  origin: Point
  radius: float

  def getPointAtAngle(self, angle: float) -> Point: ...

  @staticmethod
  def from3Points(p1: Point, p2: Point, p3: Point) -> Circle: ...
```

#### Requirements
<pre>
<a href='../pretty_trees/geometry.py#L14-L40'>Circle</a>
└── <a href='../pretty_trees/geometry.py#L5-L12'>Point</a>
</pre>

#### Dependents
<pre>
<a href='../pretty_trees/geometry.py#L14-L40'>Circle</a>
</pre>

#### Neighbors
(None)

### Config
Back to [top](#contents).

```python
from pretty_trees.config import Config
```

```python
@dataclass(frozen=True, kw_only=True)
class Config:
  branchCurvature: BranchCurvatureConfig
  startBranchState: BranchState
  endBranchState: BranchState
  offspringConfig: OffspringConfig
```

#### Requirements
<pre>
<a href='../pretty_trees/config.py#L11-L18'>Config</a>
├── <a href='../pretty_trees/config.py#L5-L9'>BranchCurvatureConfig</a>
├── <a href='../pretty_trees/branch.py#L9-L14'>BranchState</a>
└── <a href='../pretty_trees/branch.py#L16-L28'>OffspringConfig</a>
</pre>

#### Dependents
<pre>
<a href='../pretty_trees/config.py#L11-L18'>Config</a>
</pre>

#### Neighbors
(None)