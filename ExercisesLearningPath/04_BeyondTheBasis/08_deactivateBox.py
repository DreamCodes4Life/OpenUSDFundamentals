from pxr import Usd

# Open the USD stage from the specified file
file_path = "_assets/active-inactive.usda"
stage = Usd.Stage.Open(file_path)

# Iterate through all the prims on the stage
# Print the state of the stage before deactivation
print("Stage contents BEFORE deactivating:")
for prim in stage.Traverse():
    print(prim.GetPath())

# Get the "/World/Box" prim and deactivate it
box = stage.GetPrimAtPath("/World/Box")
# Passing in False to SetActive() will set the prim as Inactive and passing in True will set the prim as active
box.SetActive(False)

print("\n\nStage contents AFTER deactivating:")
for prim in stage.Traverse():
    print(prim.GetPath())