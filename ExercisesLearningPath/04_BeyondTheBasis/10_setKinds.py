from pxr import Usd, UsdGeom, Kind
import os

# File path
file_path = "_assets/kinds.usda"
if not os.path.exists(file_path):
    print(f"{file_path} not found — please run the hierarchy creation script first.")
    raise SystemExit

# Open the existing stage
stage = Usd.Stage.Open(file_path)

# -------------------------------------------------------
# Helper function to set kind safely
# -------------------------------------------------------
def set_kind(path, kind_token):
    prim = stage.GetPrimAtPath(path)
    if not prim:
        print(f"❌ Prim not found: {path}")
        return
    model_api = Usd.ModelAPI(prim)
    model_api.SetKind(kind_token)
    print(f"✅ Set kind '{kind_token}' on {path}")

# -------------------------------------------------------
# Assign kinds according to the diagram
# -------------------------------------------------------
set_kind("/Neighborhood", Kind.Tokens.assembly)
set_kind("/Neighborhood/House", Kind.Tokens.component)
set_kind("/Neighborhood/House/Window", Kind.Tokens.subcomponent)
set_kind("/Neighborhood/House/Door", Kind.Tokens.subcomponent)
set_kind("/StreetLight", Kind.Tokens.component)

# Save the stage with kind metadata
stage.GetRootLayer().Save()

# -------------------------------------------------------
# Verify the kinds and model status
# -------------------------------------------------------
print("\n--- Verification ---")
for path in [
    "/Neighborhood",
    "/Neighborhood/House",
    "/Neighborhood/House/Window",
    "/Neighborhood/House/Window/WindowPane",
    "/Neighborhood/House/Window/WindowFrame",
    "/Neighborhood/House/Door",
    "/Neighborhood/House/Door/Knob",
    "/StreetLight",
]:
    prim = stage.GetPrimAtPath(path)
    if not prim:
        continue
    model_api = Usd.ModelAPI(prim)
    kind = model_api.GetKind()
    print(f"{path:<45} kind = {kind or 'None':<15}  IsModel() = {prim.IsModel()}")

print("\n✅ Kinds set and verified.")
