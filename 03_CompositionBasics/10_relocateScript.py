from pxr import Usd, Sdf
import omni.usd

# Get stage
ctx = omni.usd.get_context()
stage = ctx.get_stage()
if not stage:
    raise Exception("No USD stage is open")

# Create namespace editor for the current edit target
editor = Usd.NamespaceEditor(stage)

old_path = Sdf.Path("/World/Green")
new_path = Sdf.Path("/World/GreenRelocated")

# Request the rename using namespace editing (will use relocates)
result = editor.MovePrimAtPath(old_path, new_path)

if not result:
    print(f"MovePrimAtPath FAILED: {result}")
else:
    print(f"MovePrimAtPath succeeded: {old_path} → {new_path}")

# Apply the edits (this actually writes relocates into the editing layer)
apply_result = editor.ApplyEdits()
if not apply_result:
    print("ApplyEdits FAILED")
else:
    print("Relocate successfully applied!")
