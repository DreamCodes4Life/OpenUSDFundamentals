# Import the necessary modules from the pxr package:
from pxr import Usd, UsdGeom

# Create a new USD stage with root layer named "xform_prim.usda":
file_path = "_assets/xform_prim.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

# Define a new Xform primitive at the path "/World" on the current stage:
world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

# Save changes to the current stage to its root layer:
stage.Save()
print(stage.ExportToString(addSourceFileComment=False))