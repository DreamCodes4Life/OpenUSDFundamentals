from pxr import Usd, UsdGeom, Sdf
from omni.usd import get_context

# ------------------------------------------------------------
# Get the CURRENT stage from Omniverse
# ------------------------------------------------------------
stage = get_context().get_stage()

# ------------------------------------------------------------
# Ensure /World exists (or create it)
# ------------------------------------------------------------
world_prim = stage.GetPrimAtPath("/World")
if not world_prim.IsValid():
    world_xform = UsdGeom.Xform.Define(stage, "/World")
else:
    world_xform = UsdGeom.Xform(world_prim)

# ------------------------------------------------------------
# Create /World/Packages
# ------------------------------------------------------------
geometry_xform = UsdGeom.Xform.Define(stage, "/World/Packages")

# ------------------------------------------------------------
# Create /World/Packages/Box and add a reference
# ------------------------------------------------------------
box_xform = UsdGeom.Xform.Define(stage, "/World/Packages/Box")
box_prim = box_xform.GetPrim()

# Add external asset reference (same as your original code)
box_prim.GetReferences().AddReference("./cubebox_a02/cubebox_a02.usd")

# ------------------------------------------------------------
# Create custom attributes on the Box prim
# ------------------------------------------------------------
weight = box_prim.CreateAttribute("acme:weight", Sdf.ValueTypeNames.Float, custom=True)
category = box_prim.CreateAttribute("acme:category", Sdf.ValueTypeNames.String, custom=True)
hazard = box_prim.CreateAttribute("acme:hazardous_material", Sdf.ValueTypeNames.Bool, custom=True)

# Add documentation for clarity (optional)
weight.SetDocumentation("The weight of the package in kilograms.")
category.SetDocumentation("The shopping category for the products this package contains.")
hazard.SetDocumentation("Whether this package contains hazardous materials.")

# Set attribute values
weight.Set(5.5)
category.Set("Cosmetics")
hazard.Set(False)

print("Custom attributes added to /World/Packages/Box")

# ------------------------------------------------------------
# No stage.Save() needed — Omniverse manages saving via UI
# ------------------------------------------------------------
