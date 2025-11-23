from pxr import Usd

# Open the USD stage from the specified file:
stage = Usd.Stage.Open("_assets/variant_prims.usda")

# List of shapes to add as variants:
shapes = ["Cube", "Sphere", "Cylinder", "Cone"]

# Get the prim at the specified path "/World/Box/Geometry":
geo_scope = stage.GetPrimAtPath("/World/Box/Geometry")

geo_variant_sets = geo_scope.GetVariantSets()
shapes_variant_set = geo_variant_sets.AddVariantSet("shapes")
for shape in shapes:
    shapes_variant_set.AddVariant(shape)

# Save the changes to the stage:
stage.Save()

# Print the USD ASCII text (like DisplayUSD(show_usd_code=True))
print(stage.GetRootLayer().ExportToString())

# Print the unflattened Root Layer:
# this only works in some environments. DisplayUSD("_assets/variant_prims.usda", show_usd_code=True)