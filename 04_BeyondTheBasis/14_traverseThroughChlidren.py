# Import the `Usd` module from the `pxr` package:
from pxr import Usd

# Open the USD stage from the specified file:
stage: Usd.Stage = Usd.Stage.Open("_assets/stage_traversal.usda")

# Get the default prim of the stage (/World in this case):
default_prim: Usd.Prim = stage.GetDefaultPrim()

# Iterate through all children of the default prim
for child in default_prim.GetAllChildren():
    # Print the path of each child prim
    print(child.GetPath())