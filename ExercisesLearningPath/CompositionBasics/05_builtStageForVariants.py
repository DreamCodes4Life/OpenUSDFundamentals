from pxr import Usd, UsdGeom

# Path to your USD file
usd_path = "_assets/variant_prims.usda"

stage: Usd.Stage = Usd.Stage.CreateNew(usd_path)

world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

box: UsdGeom.Xform = UsdGeom.Xform.Define(stage, world.GetPath().AppendPath("Box"))
geo_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, box.GetPath().AppendPath("Geometry"))

stage.Save()

# Get the USD context (the live stage in Isaac Sim)
usd_context = omni.usd.get_context()

# Open the file as the current stage
usd_context.open_stage(usd_path)