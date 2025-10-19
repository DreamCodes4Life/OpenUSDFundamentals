""" When working with large amounts of data it is key to make sure that a prim exists before trying to override it. 
We can get the child of a prim using GetChild(). If it was unable to find the child, 
it will return an invalid UsdPrim. An invalid prim will evaluate as False when treated as a boolean.
You can use Usd.Object.IsValid() to check if the prim is valid or exists. """

from pxr import Usd

file_path = "_assets/prim_hierarchy.usda"
stage: Usd.Stage = Usd.Stage.Open(file_path)

prim: Usd.Prim = stage.GetPrimAtPath("/Geometry")
child_prim: Usd.Prim
if child_prim := prim.GetChild("Box"):
    print("Child prim exists")
else:
    print("Child prim DOES NOT exist")