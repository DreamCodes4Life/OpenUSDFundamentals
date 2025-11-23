from pxr import Usd, UsdGeom

file_path = "omniverse://192.168.1.144/Youtube/References/asset_ref.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

# Define a root Xform named "World"
world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

# Define a child Xform named "Geometry" under the "World" Xform
geometry_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, world_xform.GetPath().AppendPath("Geometry"))

# Define a new Xform named "Box" under the root "Geometry" Xform
box_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, geometry_xform.GetPath().AppendPath("Box"))
box_prim: Usd.Prim = box_xform.GetPrim()

# Add a reference to a USD file containing a box geometry
box_prim.GetReferences().AddReference(
    "https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/ArchVis/Industrial/Containers/Cardboard/Cardbox_A1.usd"
)

stage.Save()