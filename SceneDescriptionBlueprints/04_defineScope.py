from pxr import Usd, UsdGeom

file_path = "_assets/scope.usda"
stage = Usd.Stage.CreateNew(file_path)

world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

# Define a new Scope primitive at the path "/World/Geometry" on the current stage:
geo_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, world.GetPath().AppendPath("Geometry"))

# Define a new Cube primitive at the path "/World/Geometry/Cube" on the current stage:
box_geo: UsdGeom.Cube = UsdGeom.Cube.Define(stage, geo_scope.GetPath().AppendPath("Cube"))

stage.Save()