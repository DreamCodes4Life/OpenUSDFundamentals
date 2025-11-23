# Import the Usd module from the pxr package
from pxr import Usd

# Open the USD stage from the specified file
stage: Usd.Stage = Usd.Stage.Open("_assets/stage_traversal.usda")

# Traverse and print the paths for the visited prims
for prim in stage.Traverse():
    # Print the path of each prim
    print(prim.GetPath())