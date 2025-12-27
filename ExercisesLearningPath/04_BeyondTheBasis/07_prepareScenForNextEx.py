from pxr import Usd, UsdGeom, UsdShade, UsdLux, Sdf, Gf
import os

# --- Config
file_path = "_assets/active-inactive.usda"

# --- Create/open stage
os.makedirs(os.path.dirname(file_path), exist_ok=True)
stage = Usd.Stage.Open(file_path) if os.path.exists(file_path) else Usd.Stage.CreateNew(file_path)

# /World
world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

# /World/Box
box = UsdGeom.Xform.Define(stage, "/World/Box")

# /World/Box/Geometry
geo = UsdGeom.Scope.Define(stage, "/World/Box/Geometry")

# /World/Box/Geometry/Cube
cube = UsdGeom.Cube.Define(stage, "/World/Box/Geometry/Cube")
cube.CreateSizeAttr(1.0)
UsdGeom.XformCommonAPI(cube).SetTranslate(Gf.Vec3d(0, 0, 0.5))

# /World/Box/Materials
mats = UsdGeom.Scope.Define(stage, "/World/Box/Materials")

# /World/Box/Materials/BoxMat
box_mat = UsdShade.Material.Define(stage, "/World/Box/Materials/BoxMat")

# (Optional) bind the empty material so hierarchy matches exactly and is ready to wire later
UsdShade.MaterialBindingAPI(cube).Bind(box_mat)

# /World/Environment
env = UsdGeom.Xform.Define(stage, "/World/Environment")

# /World/Environment/SkyLight
skylight = UsdLux.DomeLight.Define(stage, "/World/Environment/SkyLight")
skylight.CreateIntensityAttr(1000.0)

# Save
stage.Save()
print(f"Scene written to {file_path}")
