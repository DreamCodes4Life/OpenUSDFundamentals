# Import the `Usd` module from the `pxr` package:
from pxr import Usd
from pxr import UsdLux

# Define a file path name:
file_path = "_assets/schemas2.usda"
# Create a stage at the given `file_path`:
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

# Define a disk light in the stage
disk_light = UsdLux.DiskLight.Define(stage, "/World/Lights/DiskLight")
	
# Get all Attribute names that are a part of the DiskLight schema
dl_attribute_names = disk_light.GetSchemaAttributeNames()
	
# Get and Set the intensity attribute of the disk light prim
disk_light.GetIntensityAttr().Set(1000)

print(dl_attribute_names)

stage.Save()