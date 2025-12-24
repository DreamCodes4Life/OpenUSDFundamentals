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

from pxr import Kind, Sdf, Usd, UsdGeom


def position_bldg(prim: Usd.Prim, index: int):
    xform_api = UsdGeom.XformCommonAPI(prim)
    z_offset = 0.0
    rotY = 0.0
    if index > 3:
        z_offset = 200.0
        rotY = 180.0
    xform_api.SetTranslate((300.0*((index-1) % 3), 0.0, z_offset))
    xform_api.SetRotate((0.0, rotY, 0.0))


working_dir = Path(__file__).parent

asset_layer = Sdf.Layer.CreateNew(str(working_dir / "city_blockA.usd"), args={"format": "usda"})
stage = Usd.Stage.Open(asset_layer)
world_prim = UsdGeom.Xform.Define(stage, "/World").GetPrim()
stage.SetDefaultPrim(world_prim)
# PART 1
# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

Usd.ModelAPI(world_prim).SetKind(Kind.Tokens.assembly)

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE
# END PART 1

UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.centimeters)

# PART 2
# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

for x in range(1,7):
    ref_path: Sdf.Path = world_prim.GetPath().AppendChild(f"lrg_bldgF_{x:02}")
    ref_target_prim = UsdGeom.Xform.Define(stage, ref_path).GetPrim()
    ref_target_prim.GetReferences().AddReference("./lrg_bldgF/lrg_bldgF.usd")
    position_bldg(ref_target_prim, x)

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE
# END PART 2

stage.Save()