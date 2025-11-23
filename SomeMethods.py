# Import libraries from Pixar
from pxr import Usd, UsdGeom, UsdLux, UsdPhysics, Gf, Sdf, Kind

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
# Retrieve the schema info for a registered schema
Usd.SchemaRegistry.FindSchemaInfo()
# Retrieve the schema typeName
Usd.SchemaRegistry.GetSchemaTypeName()
# Used to define a new Scope at a specified path on a given stage
UsdGeom.Scope.Define(stage, path)
# This command is generic, but it's useful to confirm that a prim's type is a Scope, ensuring correct usage in scripts
prim.IsA(UsdGeom.Scope)
# Used to define a new Xform prim at a specified path on a given stage
UsdGeom.Xform.Define(stage, path)
# Retrieves the order of transformation operations, which is crucial for understanding how multiple transformations are combined. Different orders can yield different results, so understanding XformOpOrder is important. 
xform.GetXformOpOrderAttr()
# Adds a new transform operation to the Xform prim, such as translation or rotation, with specified value   
xform.AddXformOp(opType, value)
# Create a sphere light primitive
UsdLux.SphereLight.Define(stage, '/path/to/light')
# Set the intensity of a light primitive
light_prim.GetIntensityAttr().Set(500)
# Clears all content/opinions not saved on that layer
layer.Reload()
# Saves content from that layer to disk
layer.Save()
# Get a prim’s specifier
prim.GetSpecifier()
# Set a prim’s specifier
prim.SetSpecifier(specifier)
# Create a new USD stage in memory
stage = Usd.Stage.CreateInMemory()
# Check if a prim has variant sets
HasVariantSets()
# To edit a variant
SetVariantSelection()
# Constructs a UsdGeomPrimvarsAPI on UsdPrim prim
primvar_api = UsdGeom.PrimvarsAPI(prim)
# Creates a new primvar called displayColor of type Color3f[]
primvar_api.CreatePrimvar('displayColor', Sdf.ValueTypeNames.Color3fArray)
# Gets the displayColor primvar
primvar = primvar_api.GetPrimvar('displayColor')
# Sets displayColor values
primvar.Set([Gf.Vec3f(0.0, 1.0, 0.0)])
# Gets displayColor values
values = primvar.Get()
# If you need to get the same attribute value many times
UsdAttributeQuery(primvar.GetAttr()).Get()
# get the actual animated values
UsdTimeCode::EarliestTime() 
# Make the prim at /Parent inactive
stage.GetPrimAtPath('/Parent').SetActive(False)
# Return whether a prim is currently active on the stage
UsdPrim.IsActive()
# Construct a Usd.ModelAPI on a prim
prim_model_api = Usd.ModelAPI(prim)
# Return the kind of a prim
prim_model_api.GetKind()
# Set the kind of a prim to component
prim_model_api.SetKind(Kind.Tokens.component) 
# Return "true" if the prim repersents a model based on its kind metadata
prim.IsModel()  
# This yields all active, loaded, defined, non-abstract prims on this stage depth-first
Usd.Stage.Traverse()
# Traverse all prims in the stage
Usd.Stage.TraverseAll()
# Predicates are combined used bitwise operators
predicate = Usd.PrimIsActive & Usd.PrimIsLoaded
# Traverse starting from the given prim and based on the predicate for filtering the traversal
Usd.PrimRange(prim, predicate=predicate)
# You must use iter() to invoke iterator methods like Usd.PrimRange.PruneChildren()
it = iter(Usd.PrimRange.Stage(stage))
for prim in it:
    if prim.GetName() == "Environment":
        prim_range.PruneChildren()  # Skip all children of "Environment"
# remove sublayer
root_layer.subLayerPaths.remove("./contents/shading.usd")
# unload payloads (in viewport example)
stage = usdviewApi.stage
root = stage.GetPseudoRoot()
root.Unload()
# load
bldg = stage.GetPrimAtPath("/World/sm_bldgF_01")
bldg.Load()

