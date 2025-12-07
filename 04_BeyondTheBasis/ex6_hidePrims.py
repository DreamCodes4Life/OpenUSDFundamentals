from pxr import Usd, UsdGeom
from omni.usd import get_context

# ------------------------------------------------------------
# Get the CURRENT stage from Omniverse
# ------------------------------------------------------------
stage = get_context().get_stage()

if not stage:
    print("ERROR: No USD stage is currently open.")
    raise SystemExit

# ============================================================
# --- CREATE PRIM HIERARCHY (safe-define)
# ============================================================

def define_xform(path):
    """Helper to define an Xform only if not already created."""
    prim = stage.GetPrimAtPath(path)
    if not prim.IsValid():
        prim = UsdGeom.Xform.Define(stage, path).GetPrim()
    return prim

def define_scope(path):
    prim = stage.GetPrimAtPath(path)
    if not prim.IsValid():
        prim = UsdGeom.Scope.Define(stage, path).GetPrim()
    return prim

# /World
define_xform("/World")

# /World/Box
define_xform("/World/Box")

# /World/Box/Geometry
define_xform("/World/Box/Geometry")

# /World/Box/Geometry/Cube  (actual geometry point)
cube = UsdGeom.Cube.Define(stage, "/World/Box/Geometry/Cube")

# /World/Box/Materials
define_scope("/World/Box/Materials")

# /World/Box/Materials/BoxMat
define_scope("/World/Box/Materials/BoxMat")

# /World/Environment
define_xform("/World/Environment")

# /World/Environment/SkyLight
define_xform("/World/Environment/SkyLight")

print("Prim hierarchy created.\n")

# ============================================================
# --- BEFORE DEACTIVATION
# ============================================================
print("Stage contents BEFORE deactivating:")
for prim in stage.Traverse():
    print(prim.GetPath())

# ============================================================
# --- DEACTIVATE /World/Box
# ============================================================
box = stage.GetPrimAtPath("/World/Box")

if not box.IsValid():
    print("\nERROR: /World/Box does not exist.")
else:
    box.SetActive(False)
    print("\nDeactivated /World/Box")

# ============================================================
# --- AFTER DEACTIVATION
# ============================================================
print("\nStage contents AFTER deactivating:")
for prim in stage.Traverse():
    print(prim.GetPath())

# ------------------------------------------------------------
# Reminder: Omniverse handles saving via UI
# ------------------------------------------------------------
