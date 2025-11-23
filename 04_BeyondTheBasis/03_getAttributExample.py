from pxr import Usd

# Using the anmation we created in the module 1
# Open the stage
stage = Usd.Stage.Open("_assets/timecode_sample.usda")

# Get the prim
prim = stage.GetPrimAtPath("/World/Sphere")

# Get the attribute 
attr = prim.GetAttribute("xformOp:translate")

# Usd.TimeCode.Default() is implied
default_value = attr.Get()
# Get the value at time code 100.
animated_value = attr.Get(20)
print("Value at frame 20:", animated_value)
# Use EarliestTime to get earliest animated values if they exist
value = attr.Get(Usd.TimeCode.EarliestTime())
print("Earliest animated value:", value)