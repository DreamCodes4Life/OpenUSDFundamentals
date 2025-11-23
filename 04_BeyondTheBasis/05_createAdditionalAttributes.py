from pxr import Usd, UsdGeom, Sdf

file_path = "_assets/custom_attributes.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
geometry_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, world_xform.GetPath().AppendPath("Packages"))

box_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, geometry_xform.GetPath().AppendPath("Box"))
box_prim: Usd.Prim = box_xform.GetPrim()
box_prim.GetReferences().AddReference(
    "https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/ArchVis/Industrial/Containers/Cardboard/Cardbox_A1.usd"
)

# Create additional attributes for the box prim
weight = box_prim.CreateAttribute("acme:weight", Sdf.ValueTypeNames.Float, custom=True)
category = box_prim.CreateAttribute("acme:category", Sdf.ValueTypeNames.String, custom=True)
hazard = box_prim.CreateAttribute("acme:hazardous_material", Sdf.ValueTypeNames.Bool, custom=True)

# Optionally document your custom property
weight.SetDocumentation("The weight of the package in kilograms.")
category.SetDocumentation("The shopping category for the products this package contains.")
hazard.SetDocumentation("Whether this package contains hazard materials.")

# Set values for the attributes
weight.Set(5.5)
category.Set("Cosmetics")
hazard.Set(False)

# Save the stage
stage.Save()