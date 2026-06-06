# Contents
<pre>
classes
└── pretty_trees
    └── geometry.py
        └── <a href='#circle'>Circle</a>
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
<a href='../pretty_trees/geometry.py#L11-L42'>Circle</a>
└── <a href='../pretty_trees/geometry.py#L5-L9'>Point</a>
</pre>

#### Dependents
<pre>
<a href='../pretty_trees/geometry.py#L11-L42'>Circle</a>
</pre>

#### Neighbors
(None)