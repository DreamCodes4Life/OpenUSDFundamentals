#Examples include UsdLuxDiskLight, UsdLuxRectLight, and UsdLuxSphereLight.
# Import related classes
from pxr import UsdLux

# Define a disk light in the stage
disk_light = UsdLux.DiskLight.Define(stage, "/World/Lights/DiskLight")
	
# Get all Attribute names that are a part of the DiskLight schema
dl_attribute_names = disk_light.GetSchemaAttributeNames()
	
# Get and Set the intensity attribute of the disk light prim
disk_light.GetIntensityAttr().Set(1000)