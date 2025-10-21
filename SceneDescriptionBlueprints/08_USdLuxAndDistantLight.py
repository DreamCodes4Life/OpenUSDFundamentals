from pxr import Usd, UsdGeom, UsdLux, UsdShade

file_path = "_assets/distant_light.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
geo_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, world.GetPath().AppendPath("Geometry"))
box_geo: UsdGeom.Cube = UsdGeom.Cube.Define(stage, geo_scope.GetPath().AppendPath("Cube"))

# Define a new Scope primitive at the path "/World/Lights" on the current stage:
lights_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, world.GetPath().AppendPath("Lights"))

# Define a new DistantLight primitive at the path "/World/Lights/SunLight" on the current stage:
distant_light: UsdLux.DistantLight = UsdLux.DistantLight.Define(stage, lights_scope.GetPath().AppendPath("SunLight"))

stage.Save()