# Import the `Usd` module from the `pxr` package:
from pxr import Usd
from pxr import UsdGeom

# Define a file path name:
file_path = "_assets/schemas1.usda"
# Create a stage at the given `file_path`:
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

# Define a sphere in the stage
sphere = UsdGeom.Sphere.Define(stage, "/World/Sphere")
	
# Get and Set the radius attribute of the sphere
sphere.GetRadiusAttr().Set(10)

stage.Save()