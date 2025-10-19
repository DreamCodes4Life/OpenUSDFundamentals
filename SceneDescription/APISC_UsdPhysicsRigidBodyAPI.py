# Import related classes
from pxr import UsdPhysics

# Apply a UsdPhysics Rigidbody API on the cube prim
cube_rb_api = UsdPhysics.RigidBodyAPI.Apply(cube.GetPrim())
	
# Get the Kinematic Enabled Attribute 
cube_rb_api.GetKinematicEnabledAttr()
	
# Create a linear velocity attribute of value 5
cube_rb_api.CreateVelocityAttr(5)