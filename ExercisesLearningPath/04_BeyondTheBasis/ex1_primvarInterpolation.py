from pxr import Usd, UsdGeom, Gf
from omni.usd import get_context

# Get the currently opened stage in Omniverse
stage = get_context().get_stage()

# Make sure /World exists (or create it)
if not stage.GetPrimAtPath("/World"):
    world = UsdGeom.Xform.Define(stage, "/World")
else:
    world = UsdGeom.Xform(stage.GetPrimAtPath("/World"))

stage.SetDefaultPrim(world.GetPrim())

# Two-quad mesh topology (6 points, 2 faces)
mesh_vertex_locs = [
    Gf.Vec3f(-1, 0, 0),
    Gf.Vec3f(0, 0, 0),
    Gf.Vec3f(0, 1, 0),
    Gf.Vec3f(-1, 1, 0),
    Gf.Vec3f(1, 0, 0),
    Gf.Vec3f(1, 1, 0),
]

face_vertex_counts = [4, 4]
face_vertex_indices = [0, 1, 2, 3,  1, 4, 5, 2]

per_prim_color = [Gf.Vec3f(0.5, 0.0, 0.5)]
per_face_colors = [Gf.Vec3f(0.0, 0.0, 1.0), Gf.Vec3f(1.0, 0.0, 0.0)]
per_vertex_colors = [
    Gf.Vec3f(0.0, 0.0, 1.0), Gf.Vec3f(0.5, 0.0, 0.5),
    Gf.Vec3f(0.5, 0.0, 0.5), Gf.Vec3f(0.0, 0.0, 1.0),
    Gf.Vec3f(1.0, 0.0, 0.0), Gf.Vec3f(1.0, 0.0, 0.0),
]

example_meshes = {
    "PerPrim": {
        "interpolation": UsdGeom.Tokens.constant,
        "colors": per_prim_color
    },
    "PerFace": {
        "interpolation": UsdGeom.Tokens.uniform,
        "colors": per_face_colors
    },
    "PerVertex": {
        "interpolation": UsdGeom.Tokens.vertex,
        "colors": per_vertex_colors
    }
}

# Build mesh variants at 0, 2.5, and 5.0 units along X
for i, (name, data) in enumerate(example_meshes.items()):
    mesh_prim = UsdGeom.Mesh.Define(stage, f"/World/{name}")
    mesh_prim.CreatePointsAttr(mesh_vertex_locs)
    mesh_prim.CreateFaceVertexCountsAttr(face_vertex_counts)
    mesh_prim.CreateFaceVertexIndicesAttr(face_vertex_indices)
    
    # Move each mesh so they don't overlap
    UsdGeom.XformCommonAPI(mesh_prim).SetTranslate(Gf.Vec3d(i * 2.5, 0, 0))

    # Create & assign the displayColor primvar
    disp_color_primvar = mesh_prim.GetDisplayColorPrimvar() # primvars:displayColor
    disp_color_primvar.SetInterpolation(data["interpolation"])
    disp_color_primvar.Set(data["colors"])

# No need for stage.Save(); Omniverse auto-handles edits
