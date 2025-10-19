# Import related classes
from pxr import UsdGeom

# Define a sphere in the stage
sphere = UsdGeom.Sphere.Define(stage, "/World/Sphere")
	
# Get and Set the radius attribute of the sphere
sphere.GetRadiusAttr().Set(10)