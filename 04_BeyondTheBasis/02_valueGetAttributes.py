from pxr import Usd, UsdGeom

# Open a stage
stage = Usd.Stage.Open('example.usd')

# Get a prim
prim = stage.GetPrimAtPath('/World/MyPrim')

# Get an attribute
attr = prim.GetAttribute('myAttribute')
# Usd.TimeCode.Default() is implied
default_value = attr.Get()
# Get the value at time code 100.
animated_value = attr.Get(100)
# Use EarliestTime to get earliest animated values if they exist
value = attr.Get(Usd.TimeCode.EarliestTime())