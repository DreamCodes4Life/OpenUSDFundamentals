# Import the necessary modules from the `pxr` library:
from pxr import Usd, UsdGeom, Gf

# Create a new USD stage file named "timecode_sample.usda":
file_path = "_assets/timecode_sample.usda"

# Define a transform ("Xform") primitive at the "/World" path:
world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

# Define a Sphere primitive as a child of the transform at "/World/Sphere" path:
sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world.GetPath().AppendPath("Sphere"))

# Define a blue Cube as a background prim:
box: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world.GetPath().AppendPath("Backdrop"))
box.GetDisplayColorAttr().Set([(0.0, 0.0, 1.0)])
cube_xform_api = UsdGeom.XformCommonAPI(box)
cube_xform_api.SetScale(Gf.Vec3f(5, 5, 0.1))
cube_xform_api.SetTranslate(Gf.Vec3d(0, 0, -2))

# Save the stage to the file:
stage.Save()