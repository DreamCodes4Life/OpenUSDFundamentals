from pxr import Usd, UsdGeom
from omni.usd import get_context
import os

# ------------------------------------------------------------
# Helper: paths for the two sublayers we will create
# ------------------------------------------------------------
assets_dir = "_assets"
os.makedirs(assets_dir, exist_ok=True)

layer_1_path = os.path.abspath(os.path.join(assets_dir, "value_resolution_layer_1.usda"))
layer_2_path = os.path.abspath(os.path.join(assets_dir, "value_resolution_layer_2.usda"))

# ============================================================
# --- Layer 1 (weaker)
# ============================================================
layer_1_stage = Usd.Stage.CreateNew(layer_1_path)

layer_1_xform = UsdGeom.Xform.Define(layer_1_stage, "/World/XformPrim")
layer_1_xform_prim = layer_1_xform.GetPrim()

# "/World/XformPrim" customData
layer_1_xform_prim.SetCustomDataByKey("source",  "layer_1")
layer_1_xform_prim.SetCustomDataByKey("opinion", "weak")
layer_1_xform_prim.SetCustomDataByKey("unique_layer_value", "layer_1_unique_value")  # only in layer_1

# Relationship contribution from base
look_a = UsdGeom.Xform.Define(layer_1_stage, "/World/Looks/LookA")
layer_1_xform_prim.CreateRelationship("look:targets").AddTarget(look_a.GetPath())

layer_1_stage.Save()

# ============================================================
# --- Layer 2 (stronger)
# ============================================================
layer_2_stage = Usd.Stage.CreateNew(layer_2_path)

layer_2_xform = UsdGeom.Xform.Define(layer_2_stage, "/World/XformPrim")
layer_2_xform_prim = layer_2_xform.GetPrim()

# "/World/XformPrim" customData
layer_2_xform_prim.SetCustomDataByKey("source",  "layer_2")
layer_2_xform_prim.SetCustomDataByKey("opinion", "strong")

# Relationship contribution from override
look_b = UsdGeom.Xform.Define(layer_2_stage, "/World/Looks/LookB")
layer_2_xform_prim.CreateRelationship("look:targets").AddTarget(look_b.GetPath())

layer_2_stage.Save()

# ============================================================
# --- Use CURRENT STAGE as the composed stage
# ============================================================
stage = get_context().get_stage()
root_layer = stage.GetRootLayer()

# First sublayer listed is strongest → layer_2 over layer_1
root_layer.subLayerPaths = [layer_2_path, layer_1_path]

# Now read the composed prim from the current stage
xform_prim = stage.GetPrimAtPath("/World/XformPrim")
if not xform_prim:
    print("WARNING: /World/XformPrim not found on the composed stage.")
else:
    resolved_custom_data = xform_prim.GetCustomData()

    print("Resolved CustomData:")
    for key, value in resolved_custom_data.items():
        print(f"- '{key}': '{value}'")

    # resolved relationship targets:
    targets = xform_prim.GetRelationship("look:targets").GetTargets()
    print(f"\nResolved relationship targets: {[str(t) for t in targets]}")  # should see both LookA and LookB

# ============================================================
# --- Optional: write out the composed result to inspect
# ============================================================
explicit_composed_path = os.path.abspath(
    os.path.join(assets_dir, "value_resolution_composed_explicit.usda")
)
txt = stage.ExportToString(addSourceFileComment=False)
with open(explicit_composed_path, "w") as f:
    f.write(txt)

print(f"\nWrote explicit composed stage to: {explicit_composed_path}")
print(f"Layer 1: {layer_1_path}")
print(f"Layer 2: {layer_2_path}")
