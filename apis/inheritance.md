# Contents
<pre>
classes
└── pretty_trees
    ├── branch.py
    │   └── <a href='#branch'>Branch</a>
    └── branch_texture.py
        └── <a href='#solidcolorbranchtexture'>SolidColorBranchTexture</a>
</pre>

### Branch
Back to [top](#contents).

```python
from pretty_trees.branch import Branch
```

```python
class Branch:
  ...
```

#### Requirements
<pre>
<a href='../pretty_trees/branch.py#L1-L3'>Branch</a>
</pre>

#### Dependents
<pre>
<a href='../pretty_trees/branch.py#L1-L3'>Branch</a>
</pre>

#### Neighbors
(None)

### SolidColorBranchTexture
Back to [top](#contents).

```python
from pretty_trees.branch_texture import SolidColorBranchTexture
```

```python
class SolidColorBranchTexture:
  def __init__(self, color: Color) -> None: ...

  def createSprite(self, position: Point, batch: Batch, program: ShaderProgram) -> Sprite: ...
```

#### Requirements
<pre>
<a href='../pretty_trees/branch_texture.py#L10-L29'>SolidColorBranchTexture</a>
</pre>

#### Dependents
<pre>
<a href='../pretty_trees/branch_texture.py#L10-L29'>SolidColorBranchTexture</a>
</pre>

#### Neighbors
(None)