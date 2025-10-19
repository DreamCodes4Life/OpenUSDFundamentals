# Used to define a new Scope at a specified path on a given stage
UsdGeom.Scope.Define(stage, path)

# This command is generic, but it's useful to confirm that a prim's type is a Scope, ensuring correct usage in scripts
prim.IsA(UsdGeom.Scope)