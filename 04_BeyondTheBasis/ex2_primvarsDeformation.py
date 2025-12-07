from pxr import Usd, UsdGeom, Sdf, Gf
from omni.usd import get_context

# -------------------------------------------------------------------
# 1. Get the current stage instead of creating a new one
# -------------------------------------------------------------------
stage = get_context().get_stage()

# Set up time sampling parameters
start_tc = 1
end_tc = 90
time_code_per_second = 30

stage.SetStartTimeCode(start_tc)
stage.SetEndTimeCode(end_tc)
stage.SetTimeCodesPerSecond(time_code_per_second)

# -------------------------------------------------------------------
# 2. Make sure /World exists (or create it)
# -------------------------------------------------------------------
world_prim = stage.GetPrimAtPath("/World")
if not world_prim:
    world = UsdGeom.Xform.Define(stage, "/World")
else:
    world = UsdGeom.Xform(world_prim)

stage.SetDefaultPrim(world.GetPrim())

# -------------------------------------------------------------------
# 3. Define base mesh (a simple quad)
# -------------------------------------------------------------------
mesh_vertex_locs = [
    Gf.Vec3f(0, 0, 0),
    Gf.Vec3f(1, 0, 0),
    Gf.Vec3f(1, 1, 0),
    Gf.Vec3f(0, 1, 0)
]
face_vertex_counts = [4]
face_vertex_indices = [0, 1, 2, 3]

# -------------------------------------------------------------------
# 4. Create mesh prim under /World
# -------------------------------------------------------------------
plane = UsdGeom.Mesh.Define(stage, world.GetPath().AppendPath("Plane"))
plane.CreatePointsAttr(mesh_vertex_locs)
plane.CreateFaceVertexCountsAttr(face_vertex_counts)
plane.CreateFaceVertexIndicesAttr(face_vertex_indices)

# Move it a bit so you can see it clearly
UsdGeom.XformCommonAPI(plane).SetTranslate(Gf.Vec3d(0, 0, 0))

# Give it a base display color
plane.GetDisplayColorPrimvar().Set([Gf.Vec3f(1, 0, 0)])

# -------------------------------------------------------------------
# 5. Create a "rest_state" primvar (the original, undeformed positions)
# -------------------------------------------------------------------
plane_privar_api = UsdGeom.PrimvarsAPI(plane)
plane_privar_api.CreatePrimvar(
    "rest_state",
    Sdf.ValueTypeNames.Float3Array,
    UsdGeom.Tokens.vertex
).Set(mesh_vertex_locs)

# -------------------------------------------------------------------
# 6. Create a "deformation" primvar (offsets per vertex)
# -------------------------------------------------------------------
deformation = [
    Gf.Vec3f(0.0, 0.0, 0.0),
    Gf.Vec3f(-0.3, 0.4, 0.0),
    Gf.Vec3f(-0.3, 0.4, 0.0),
    Gf.Vec3f(0.0, 0.0, 0.0),
]

plane_privar_api.CreatePrimvar(
    "deformation",
    Sdf.ValueTypeNames.Float3Array,
    UsdGeom.Tokens.vertex
).Set(deformation)

# Compute new, deformed points = rest_state + deformation
new_points = [
    p + o for p, o in zip(
        mesh_vertex_locs,
        plane_privar_api.GetPrimvar("deformation").Get()
    )
]

print("Original vertex locations:", mesh_vertex_locs)
print("\nDeforming mesh with primvar 'deformation':", deformation)
print("\nNew vertex locations:", new_points)

# -------------------------------------------------------------------
# 7. Time-sample Mesh.points from rest to deformed
# -------------------------------------------------------------------
plane_points = plane.GetPointsAttr()
plane_points.Set(mesh_vertex_locs, Usd.TimeCode(start_tc))   # frame 1
plane_points.Set(new_points, Usd.TimeCode(end_tc))           # frame 90

# No stage.Save() here – you save from the Omniverse UI if you want
