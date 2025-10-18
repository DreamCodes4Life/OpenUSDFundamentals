from pxr import Usd, UsdGeom, Gf

file_path = "_assets/attributes_ex1.usda"

stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

# Define a sphere under the World xForm:
sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world_xform.GetPath().AppendPath("Sphere"))

# Define a cube under the World xForm and set it to be 5 units away from the sphere:
cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendPath("Cube"))
UsdGeom.XformCommonAPI(cube).SetTranslate(Gf.Vec3d(5, 0, 0))

# Get the property names of the cube prim:
cube_prop_names = cube.GetPrim().GetPropertyNames()

# Print the property names:
for prop_name in cube_prop_names:
    print(prop_name)

stage.Save()