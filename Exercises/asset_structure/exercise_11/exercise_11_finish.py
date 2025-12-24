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

from enum import Enum
from pathlib import Path

from pxr import Kind, Sdf, Usd, UsdGeom

class Side(Enum):
    North = 1
    South = 2

### UPDATED - Added side parameter
def position_bldg(prim: Usd.Prim, index: int, side: Side):
    xform_api = UsdGeom.XformCommonAPI(prim)
    z_offset = 0.0
    rotY = 0.0
    ### UPDATED - Replaced index with side
    if side == Side.South:
        z_offset = 200.0
        rotY = 180.0
    ### UPDATED - Removed modulus
    xform_api.SetTranslate((300.0*(index-1), 0.0, z_offset))
    xform_api.SetRotate((0.0, rotY, 0.0))


working_dir = Path(__file__).parent

asset_layer = Sdf.Layer.CreateNew(str(working_dir / "city_blockA.usd"), args={"format": "usda"})
stage = Usd.Stage.Open(asset_layer)
world_prim = UsdGeom.Xform.Define(stage, "/World").GetPrim()
stage.SetDefaultPrim(world_prim)
Usd.ModelAPI(world_prim).SetKind(Kind.Tokens.assembly)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.centimeters)

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

### Update - Added for loop for street sides
for side in Side:
    ### Update - Added an intermediate group prim between /World and the building references.
    side_xform = UsdGeom.Xform.Define(stage, world_prim.GetPath().AppendChild(side.name))
    Usd.ModelAPI(side_xform).SetKind(Kind.Tokens.group)
    for x in range(1,4):
        ref_path: Sdf.Path = side_xform.GetPath().AppendChild(f"lrg_bldgF_{x:02}")
        ref_target_prim = UsdGeom.Xform.Define(stage, ref_path).GetPrim()
        ref_target_prim.GetReferences().AddReference("./lrg_bldgF/lrg_bldgF.usd")
        position_bldg(ref_target_prim, x, side)

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE

stage.Save()