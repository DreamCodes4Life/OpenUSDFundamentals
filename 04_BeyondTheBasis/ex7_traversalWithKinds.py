from pxr import Usd, UsdGeom, Kind, Gf
from omni.usd import get_context

# -------------------------------------------------------------
# Get the current stage
# -------------------------------------------------------------
stage = get_context().get_stage()

# -------------------------------------------------------------
# Ensure /World exists
# -------------------------------------------------------------
world_prim = stage.GetPrimAtPath("/World")
if not world_prim:
    world_xform = UsdGeom.Xform.Define(stage, "/World")
else:
    world_xform = UsdGeom.Xform(world_prim)

stage.SetDefaultPrim(world_xform.GetPrim())

# Make /World a group so its children can be models
Usd.ModelAPI(world_xform.GetPrim()).SetKind(Kind.Tokens.group)

# -------------------------------------------------------------
# Non-model branch: Markers
# -------------------------------------------------------------
markers = UsdGeom.Scope.Define(stage, world_xform.GetPath().AppendChild("Markers"))

points = {
    "PointA": Gf.Vec3d(-3, 0, -3),
    "PointB": Gf.Vec3d(-3, 0, 3),
    "PointC": Gf.Vec3d(3, 0, -3),
    "PointD": Gf.Vec3d(3, 0, 3),
}

for name, pos in points.items():
    cone = UsdGeom.Cone.Define(stage, markers.GetPath().AppendChild(name))
    # Make the cone axis Y instead of default Z
    cone.CreateAxisAttr().Set("Y")
    UsdGeom.XformCommonAPI(cone).SetTranslate(pos)
    cone.CreateDisplayColorPrimvar().Set([Gf.Vec3f(1.0, 0.85, 0.2)])

# -------------------------------------------------------------
# Model branch: a Component model
# -------------------------------------------------------------
component = UsdGeom.Xform.Define(stage, world_xform.GetPath().AppendChild("Component"))
Usd.ModelAPI(component.GetPrim()).SetKind(Kind.Tokens.component)

body = UsdGeom.Cube.Define(stage, component.GetPath().AppendChild("Body"))
body.CreateDisplayColorPrimvar().Set([(0.25, 0.55, 0.85)])
UsdGeom.XformCommonAPI(body).SetScale((3.0, 1.0, 3.0))

# -------------------------------------------------------------
# Model traversal: affect ONLY model prims, skip Markers
# -------------------------------------------------------------
for prim in Usd.PrimRange(stage.GetPseudoRoot(), predicate=Usd.PrimIsModel):

    # Only apply transforms to components
    if prim.IsComponent():
        xformable = UsdGeom.Xformable(prim)
        UsdGeom.XformCommonAPI(xformable).SetTranslate((0.0, 2.0, 0.0))

# -------------------------------------------------------------
# Print which prims USD considers models
# -------------------------------------------------------------
model_paths = [
    p.GetPath().pathString
    for p in Usd.PrimRange(stage.GetPseudoRoot(), predicate=Usd.PrimIsModel)
]

print("Model prims seen by traversal:", model_paths)

# No stage.Save() needed — Omniverse manages saving
