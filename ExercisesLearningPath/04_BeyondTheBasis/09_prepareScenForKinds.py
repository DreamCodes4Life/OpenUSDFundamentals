from pxr import Usd, UsdGeom
import os

file_path = "_assets/kinds.usda"
os.makedirs(os.path.dirname(file_path), exist_ok=True)

# Open if it exists, otherwise create
stage = Usd.Stage.Open(file_path) if os.path.exists(file_path) else Usd.Stage.CreateNew(file_path)

# ----- Hierarchy (no kinds set) -----
# /Neighborhood (root group)
neighborhood = UsdGeom.Xform.Define(stage, "/Neighborhood")
stage.SetDefaultPrim(neighborhood.GetPrim())

# /Neighborhood/House
house = UsdGeom.Xform.Define(stage, "/Neighborhood/House")

# /Neighborhood/House/Window
window = UsdGeom.Xform.Define(stage, "/Neighborhood/House/Window")
UsdGeom.Xform.Define(stage, "/Neighborhood/House/Window/WindowPane")
UsdGeom.Xform.Define(stage, "/Neighborhood/House/Window/WindowFrame")

# /Neighborhood/House/Door
door = UsdGeom.Xform.Define(stage, "/Neighborhood/House/Door")
UsdGeom.Xform.Define(stage, "/Neighborhood/House/Door/Knob")

# /StreetLight (sibling at root)
street_light = UsdGeom.Xform.Define(stage, "/StreetLight")

# Save
stage.GetRootLayer().Save()
print(f"✅ Scene written to {file_path}")
