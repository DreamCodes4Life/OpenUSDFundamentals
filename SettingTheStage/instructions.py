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