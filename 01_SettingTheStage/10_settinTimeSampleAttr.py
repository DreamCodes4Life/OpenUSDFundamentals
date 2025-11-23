from pxr import Usd, UsdGeom

stage: Usd.Stage = Usd.Stage.Open("_assets/timecode_sample.usda")
world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world.GetPath().AppendPath("Sphere"))
box: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world.GetPath().AppendPath("Backdrop"))
box.GetDisplayColorAttr().Set([(0.0, 0.0, 1.0)])
cube_xform_api = UsdGeom.XformCommonAPI(box)
cube_xform_api.SetScale(Gf.Vec3f(5, 5, 0.1))
cube_xform_api.SetTranslate(Gf.Vec3d(0, 0, -2))

stage.SetStartTimeCode(1)
stage.SetEndTimeCode(60)

if translate_attr := sphere.GetTranslateOp().GetAttr():
    translate_attr.Clear()
if scale_attr := sphere.GetScaleOp().GetAttr():
    scale_attr.Clear()

sphere_xform_api = UsdGeom.XformCommonAPI(sphere)

sphere_xform_api.SetTranslate(Gf.Vec3d(0,  5.50, 0), time=1)  
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -4.50, 0), time=30)  
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -5.00, 0), time=45)  
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -3.25, 0), time=50)  
sphere_xform_api.SetTranslate(Gf.Vec3d(0,  5.50, 0), time=60)  

# Set scale of the sphere at time 1
sphere_xform_api.SetScale(Gf.Vec3f(1.00, 1.00, 1.00), time=1)  
# Set scale of the sphere at time 30
sphere_xform_api.SetScale(Gf.Vec3f(1.00, 1.00, 1.00), time=30)   
# Set scale of the sphere at time 45
sphere_xform_api.SetScale(Gf.Vec3f(1.00, 0.20, 1.25), time=45)   
# Set scale of the sphere at time 50
sphere_xform_api.SetScale(Gf.Vec3f(0.75, 2.00, 0.75), time=50)  
# Set scale of the sphere at time 60
sphere_xform_api.SetScale(Gf.Vec3f(1.00, 1.00, 1.00), time=60)  

# Export to a new flattened layer for this example.
stage.Export("_assets/timecode_ex2b.usda", addSourceFileComment=False)