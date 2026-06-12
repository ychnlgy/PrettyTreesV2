# Contents
<pre>
classes
└── pretty_trees
    ├── branch.py
    │   └── <a href='#branch'>Branch</a>
    ├── branch_texture.py
    │   └── <a href='#branchtextureinterface'>BranchTextureInterface</a>
    └── sprite_factory.py
        └── <a href='#spritefactoryinterface'>SpriteFactoryInterface</a>
</pre>

### Branch
Back to [top](#contents).

```python
from pretty_trees.branch import Branch
```

```python
class Branch:
  def __init__(self, spriteFactory: BranchSpriteFactory, position: Point, startState: BranchState, endState: BranchState) -> None: ...

  def grow(self, food: float, offspringConfig: OffspringConfig) -> None: ...

  def setPosition(self, position: Point) -> None: ...
```

#### Requirements
<pre>
<a href='../pretty_trees/branch.py#L30-L127'>Branch</a>
</pre>

#### Dependents
<pre>
<a href='../pretty_trees/branch.py#L30-L127'>Branch</a>
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

  @abstractmethod
  def getDimensions(self) -> tuple[float, float]: ...
```

#### Requirements
<pre>
<a href='../pretty_trees/branch_texture.py#L12-L25'>BranchTextureInterface</a>
</pre>

#### Dependents
<pre>
<a href='../pretty_trees/branch_texture.py#L12-L25'>BranchTextureInterface</a>
└── <a href='../pretty_trees/branch_texture.py#L27-L50'>SolidColorBranchTexture</a>
</pre>

#### Neighbors
| Neighbor | Similarity | Common Properties |
| --- | --- | --- |
| <a href='../pretty_trees/sprite_factory.py#L9-L17'>SpriteFactoryInterface</a> | 50% | `getDimensions` |

### SpriteFactoryInterface
Back to [top](#contents).

```python
from pretty_trees.sprite_factory import SpriteFactoryInterface
```

```python
class SpriteFactoryInterface(ABC):
  @abstractmethod
  def create(self, position: Point) -> Sprite: ...

  @abstractmethod
  def getDimensions(self) -> tuple[float, float]: ...
```

#### Requirements
<pre>
<a href='../pretty_trees/sprite_factory.py#L9-L17'>SpriteFactoryInterface</a>
</pre>

#### Dependents
<pre>
<a href='../pretty_trees/sprite_factory.py#L9-L17'>SpriteFactoryInterface</a>
└── <a href='../pretty_trees/sprite_factory.py#L19-L39'>BranchSpriteFactory</a>
</pre>

#### Neighbors
| Neighbor | Similarity | Common Properties |
| --- | --- | --- |
| <a href='../pretty_trees/branch_texture.py#L12-L25'>BranchTextureInterface</a> | 50% | `getDimensions` |