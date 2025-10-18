# Import the `Usd` module from the `pxr` package:
from pxr import Usd

# Define a file path name:
file_path = "_assets/first_stage.usda"
# Create a stage at the given `file_path`:
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)
print(stage.ExportToString(addSourceFileComment=False))