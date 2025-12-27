from pxr import Usd, UsdGeom

# Create a stage and define a prim path
stage = Usd.Stage.CreateNew('_assets/example.usda')
prim = UsdGeom.Xform.Define(stage, '/ExamplePrim')

# Check if the XformCommonAPI is compatible with the prim using the bool operator 
if not (xform_api := UsdGeom.XformCommonAPI(prim)):
    raise Exception("Prim not compatible with XformCommonAPI")

# Set transformations
xform_api.SetTranslate((10.0, 20.0, 30.0))
xform_api.SetRotate((45.0, 0.0, 90.0), UsdGeom.XformCommonAPI.RotationOrderXYZ)
xform_api.SetScale((2.0, 2.0, 2.0))