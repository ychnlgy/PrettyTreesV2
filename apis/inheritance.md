# Contents
<pre>
classes
└── pretty_trees
    ├── branch.py
    │   └── <a href='#branch'>Branch</a>
    ├── branch_texture.py
    │   └── <a href='#branchtextureinterface'>BranchTextureInterface</a>
    └── tree.py
        └── <a href='#tree'>Tree</a>
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

### BranchTextureInterface
Back to [top](#contents).

```python
from pretty_trees.branch_texture import BranchTextureInterface
```

```python
class BranchTextureInterface(ABC):
  @abstractmethod
  def createSprite(self, position: Point, batch: Batch, program: ShaderProgram) -> Sprite: ...
```

#### Requirements
<pre>
<a href='../pretty_trees/branch_texture.py#L12-L21'>BranchTextureInterface</a>
</pre>

#### Dependents
<pre>
<a href='../pretty_trees/branch_texture.py#L12-L21'>BranchTextureInterface</a>
└── <a href='../pretty_trees/branch_texture.py#L23-L43'>SolidColorBranchTexture</a>
</pre>

#### Neighbors
(None)

### Tree
Back to [top](#contents).

```python
from pretty_trees.tree import Tree
```

```python
class Tree:
  def __init__(self, batch: Batch, shaderProgram: ShaderProgram, branchTexture: BranchTextureInterface) -> None: ...

  def addBranch(self, position: Point) -> None: ...

  def update(self, dt: float) -> None: ...
```

#### Requirements
<pre>
<a href='../pretty_trees/tree.py#L7-L30'>Tree</a>
</pre>

#### Dependents
<pre>
<a href='../pretty_trees/tree.py#L7-L30'>Tree</a>
</pre>

#### Neighbors
(None)