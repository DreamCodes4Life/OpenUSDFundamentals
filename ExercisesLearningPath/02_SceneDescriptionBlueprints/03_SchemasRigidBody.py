# Import the `Usd` module from the `pxr` package:
from pxr import Usd, UsdGeom, UsdLux, UsdPhysics, Gf

# Define a file path name:
file_path = "_assets/schemas4.usda"
# Create a stage at the given `file_path`:
stage: Usd.Stage = Usd.Stage.Open(file_path)
world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendPath("Box"))
sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world_xform.GetPath().AppendPath("Sphere"))
UsdGeom.XformCommonAPI(sphere).SetTranslate(Gf.Vec3d(5, 0, 0))

# Apply a UsdPhysics Rigidbody API on the cube prim
primCube = cube.GetPrim()
cube_rb_api = UsdPhysics.RigidBodyAPI.Apply(primCube)
	
# Get the Kinematic Enabled Attribute 
kin = cube_rb_api.GetKinematicEnabledAttr()

print("prim path: ", primCube)
print(f"kin: {kin.Get()}")

# Create a linear velocity attribute of value 5
cube_rb_api.CreateVelocityAttr(Gf.Vec3f(5.0, 0.0, 0.0))

stage.Save()