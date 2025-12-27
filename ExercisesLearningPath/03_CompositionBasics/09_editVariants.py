from pxr import Usd

# Open the USD stage from the specified file:
stage = Usd.Stage.Open("_assets/variant_prims.usda")

# List of shapes to add as variants:
shapes = ["Cube", "Sphere", "Cylinder", "Cone"]

# Get the prim at the specified path "/World/Box/Geometry":
geo_scope = stage.GetPrimAtPath("/World/Box/Geometry")

# Get the "shapes" variant set for the geometry scope:
geo_variant_sets = geo_scope.GetVariantSets()
shapes_variant_set = geo_variant_sets.AddVariantSet("shapes")
    
# Loop over each shape in the list of shapes
for shape in shapes:
    # Print the shape being added
    print("adding: " + shape)
    
    # Add a variant named after the shape to the "shapes" variant set
    shapes_variant_set.AddVariant(shape)
    
    # Select the current variant for editing
    shapes_variant_set.SetVariantSelection(shape)
    
    # Enter the variant edit context to make changes specific to the current variant
    with shapes_variant_set.GetVariantEditContext():
        # Define a new prim for the current shape under the geometry scope
        shape_prim = stage.DefinePrim(geo_scope.GetPath().AppendPath(shape))
        
        # Set the type of the new prim to the current shape
        shape_prim.SetTypeName(shape)


# Here we define what Variant from the VariantSet is selected. Change this between "Cube", "Sphere", "Cylinder", and "Cone"
# to see the different geometries:
shapes_variant_set.SetVariantSelection("Cube")
# shapes_variant_set.SetVariantSelection("Sphere")
# shapes_variant_set.SetVariantSelection("Cylinder")
# shapes_variant_set.SetVariantSelection("Cone")

# Save the changes to the stage
stage.Save()

# Print the USD ASCII text (like DisplayUSD(show_usd_code=True))
print(stage.GetRootLayer().ExportToString())