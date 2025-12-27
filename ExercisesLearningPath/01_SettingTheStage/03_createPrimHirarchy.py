from pxr import Usd, UsdGeom

file_path = "_assets/prim_hierarchy.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

# Define a Scope prim in stage at `/Geometry`
geom_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, "/Geometry")
# Define an Xform prim in the stage as a child of /Geometry called GroupTransform
xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, geom_scope.GetPath().AppendPath("GroupTransform"))
# Define a Cube in the stage as a child of /Geometry/GroupTransform, called Box
cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, xform.GetPath().AppendPath("Box"))

stage.Save()