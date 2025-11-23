# Import the Usd module from the pxr package
from pxr import Usd

# Open the USD stage from the specified file
stage: Usd.Stage = Usd.Stage.Open("_assets/stage_traversal.usda")

prim_range = Usd.PrimRange(stage.GetPrimAtPath("/World/Box"))
for prim in prim_range:
    print(prim.GetPath())