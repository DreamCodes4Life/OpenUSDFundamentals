from pathlib import Path
from pxr import Usd, Sdf

working_dir = Path(__file__).parent

stage = Usd.Stage.Open(str(working_dir / "my_skyscraper.usda"))

root_layer: Sdf.Layer = stage.GetRootLayer()
sublayers = root_layer.subLayerPaths