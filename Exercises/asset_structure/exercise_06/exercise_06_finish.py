# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path

from pxr import Sdf, Usd, UsdGeom

working_dir = Path(__file__).parent

# PART 1
# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

stage: Usd.Stage = Usd.Stage.Open(str(working_dir / "lrg_bldgF.usd"))
# "Save As..." the lrg_bldgF.usd as contents.usd
asset_layer: Sdf.Layer = stage.GetRootLayer()
contents_layer_name = "contents.usd"
asset_layer.Export(str(working_dir / contents_layer_name), args={"format": "usda"})

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE
# END PART 1 

# PART 2
# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

# Create a new asset_layer in memory for now.
stage: Usd.Stage = Usd.Stage.CreateInMemory()
world_prim = UsdGeom.Xform.Define(stage, "/World").GetPrim()
stage.SetDefaultPrim(world_prim)
UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.centimeters)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

# Add contents.usd as a payload
world_prim.GetPayloads().AddPayload(f"./{contents_layer_name}")
stage.GetRootLayer().Export(str(working_dir / "lrg_bldgF.usd"), args={"format": "usda"})

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE
# END PART 2 