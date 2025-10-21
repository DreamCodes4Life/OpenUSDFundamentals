from pxr import Usd

# Open the USD stage from the specified file:
stage = Usd.Stage.Open("_assets/variant_prims.usda")

# Get the prim at the specified path:
geo_scope = stage.GetPrimAtPath("/World/Box/Geometry")

# Get the "shapes" variant set for the geometry scope:
geo_variant_sets = geo_scope.GetVariantSets()
shapes_variant_set = geo_variant_sets.AddVariantSet("shapes")

# Add a variant named "Cube" to the "shapes" variant set:
geo_variant_set.AddVariant("Cube")

# Print whether the geometry scope now has variant sets:
print(geo_scope.HasVariantSets())

# Save the changes to the stage:
stage.Save()