from pxr import Usd, UsdGeom, Gf

# Create a new stage and define a cube:
file_path = "omniverse://192.168.1.144/Youtube/References/cube2.usda"
stage = Usd.Stage.CreateNew(file_path)
cube = UsdGeom.Cube.Define(stage, "/Cube2")
stage.SetDefaultPrim(cube.GetPrim())
stage.Save()

# Note: Create the first file first, then the second.

# Create a second file path and stage, define a world and a sphere:
second_file_path = "omniverse://192.168.1.144/Youtube/References/shapes2.usda"
stage = Usd.Stage.CreateNew(second_file_path)
world = UsdGeom.Xform.Define(stage, "/World2")
UsdGeom.Sphere.Define(stage, world.GetPath().AppendPath("Sphere2"))

# Define a reference prim and set its translation:
reference_prim = stage.DefinePrim(world.GetPath().AppendPath("Cube_Ref2"))

# Add a reference to the "cube.usda" file:
reference_prim.GetReferences().AddReference("./cube2.usda")
# Position the cube
UsdGeom.XformCommonAPI(reference_prim).SetTranslate(Gf.Vec3d(5, 0, 0))

stage.Save()