# Import the `Usd` module from the `pxr` package:
from pxr import Usd

# Create a new USD stage with root layer named "prims.usda":
stage: Usd.Stage = Usd.Stage.CreateNew("_assets/prims.usda")

# Define a new primitive at the path "/hello" on the current stage:
stage.DefinePrim("/hello")

# Define a new primitive at the path "/world" on the current stage with the prim type, Sphere.
stage.DefinePrim("/world", "Sphere")

stage.Save()