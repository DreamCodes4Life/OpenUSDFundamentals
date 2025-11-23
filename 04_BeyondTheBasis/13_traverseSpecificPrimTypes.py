# Import necessary modules from the pxr package
from pxr import Usd, UsdGeom

# Open the USD stage from the specified file
stage: Usd.Stage = Usd.Stage.Open("_assets/stage_traversal.usda")

scope_count = 0
xform_count = 0
# Traverse through each prim in the stage
for prim in stage.Traverse():
    # Check if the prim is of type Scope
    if UsdGeom.Scope(prim):
        scope_count += 1
        print("Scope Type: ", prim.GetName())
    # Check if the prim is of type Xform
    elif UsdGeom.Xform(prim):
        xform_count +=1
        print("Xform Type: ", prim.GetName())

print("Number of Scope prims: ", scope_count)
print("Number of Xform prims: ", xform_count)