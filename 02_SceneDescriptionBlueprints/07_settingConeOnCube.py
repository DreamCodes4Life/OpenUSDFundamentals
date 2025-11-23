from pxr import Usd, UsdGeom

file_path = "_assets/xformcommonapi.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

cone: UsdGeom.Cone = UsdGeom.Cone.Define(stage, "/Cone")
box: UsdGeom.Cube = UsdGeom.Cube.Define(stage, "/Cube")

cone.GetDisplayColorAttr().Set([(1.0, 0.5, 0.25)])
# Create an API object for the prim we want to manipulate
cone_xform_api = UsdGeom.XformCommonAPI(cone)
# Scale the cone to half its original size about the center of the cone.
cone_xform_api.SetScale((0.5, 0.5, 0.5))
# Move the cone up 1.5 meters: (half the cube's size + half the scaled cone's height) = (1.0 + 0.5)
cone_xform_api.SetTranslate((0.0, 1.5, 0.0))

stage.Save()