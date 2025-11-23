from pxr import Usd, UsdGeom, UsdShade, UsdLux
import os

# --- Path
file_path = "_assets/stage_traversal.usda"
os.makedirs(os.path.dirname(file_path), exist_ok=True)

# --- Create stage
stage = Usd.Stage.CreateNew(file_path)

# /World (defaultPrim)
world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

# /World/Box
box = UsdGeom.Xform.Define(stage, "/World/Box")

# /World/Box/Geometry
geo = UsdGeom.Scope.Define(stage, "/World/Box/Geometry")

# /World/Box/Geometry/Cube
UsdGeom.Cube.Define(stage, "/World/Box/Geometry/Cube")

# /World/Box/Materials
mats = UsdGeom.Scope.Define(stage, "/World/Box/Materials")

# /World/Box/Materials/BoxMat
UsdShade.Material.Define(stage, "/World/Box/Materials/BoxMat")

# /World/Environment
env = UsdGeom.Scope.Define(stage, "/World/Environment")

# /World/Environment/SkyLight (DistantLight)
UsdLux.DistantLight.Define(stage, "/World/Environment/SkyLight")

# Save
stage.GetRootLayer().Save()
print(f"Wrote {file_path}")
