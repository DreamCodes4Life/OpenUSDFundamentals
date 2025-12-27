from pxr import Usd

# Open the USD stage from the specified file:
stage = Usd.Stage.Open("_assets/variant_prims.usda")

# Get the prim at the specified path:
geo_scope = stage.GetPrimAtPath("/World/Box/Geometry")

# Print whether the prim has variant sets:
print(geo_scope.HasVariantSets())