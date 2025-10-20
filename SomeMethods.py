# Import Usd, Sdf, and Gf libraries from Pixar
from pxr import Usd, Sdf, Gf

# Create a new, empty USD stage where 3D scenes are assembled
Usd.Stage.CreateNew()
# Open an existing USD file as a stage
Usd.Stage.Open()
# Saves all layers in a USD stage
Usd.Stage.Save()
# Generic USD API command. Used to define a new prim on a stage at a specified path, and optionally the type of prim.
stage.DefinePrim(path, prim_type)
# Specific to UsdGeom schema. Used to define a new prim on a USD stage at a specified path of type Xform. 
UsdGeom.Xform.Define(stage, path)
# Retrieves the children of a prim. Useful for navigating through the scenegraph.
prim.GetChildren()
# Returns the type of the prim, helping identify what kind of data the prim contains.
prim.GetTypeName()
# Returns all properties of the prim.
prim.GetProperties()
# Get the radius value of sphere_prim that is of type UsdGeom.Sphere
sphere_prim.GetRadiusAttr().Get()
# Set the double-sided property of the prim
sphere_prim.GetDoubleSidedAttr().Set(True)
# Get the target paths of a relationship
UsdRelationship.GetTargets()
# Set the target paths for a relationship
UsdRelationship.SetTargets()
# Add a new target path to a relationship
UsdRelationship.AddTarget()
# Remove a target path from a relationship
UsdRelationship.RemoveTarget()
# Returns authored TimeSamples
cube.GetDisplayColorAttr().GetTimeSamples()
# Sets TimeSample Value (Gf.Vec3d(0,-4.5,0)) at a specified TimeCode (30)
sphere_xform_api.SetTranslate(Gf.Vec3d(0,-4.5,0), time=Usd.TimeCode(30))
# Get the size attribute of the cube
cube_size_attr: Usd.Attribute = cube_prim.GetSizeAttr()
# Set the size of the cube at time=1 to 1
cube_size_attr.Set(time=1, value=1)
# Set the size of the cube at time=60 to 10
cube_size_attr.Set(time=60, value=10)
# Return the path of a Usd.Prim as an Sdf.Path object
Usd.Prim.GetPath()
# Retrieve a Usd.Prim at the specified path from the Stage
Usd.Stage.GetPrimAtPath()
# Retrieve the metadata value associated with the given key for a USD Object
usdobject.GetMetadata('key')
# Set the metadata value for the given key on a USD Object
usdobject.SetMetadata('key', value)
# Retrieve the metadata value associated with the given key for the stage
stage.GetMetadata('key')
# Set the metadata value for the given key on the stage
stage.SetMetadata('key', value) 
# Use for better performance if accessing a single value and not all the metadata within a key
GetMetadataByDictKey()