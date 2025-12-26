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

import json
from pathlib import Path

from pxr import Usd, UsdGeom, Gf, Sdf

exercise_dir = Path(__file__).parent

with open(str(exercise_dir / "points_export.json")) as f:
    export_data = json.load(f)

stage = Usd.Stage.Open(str(exercise_dir / "Scenario.usd"))
stage_path = Path(stage.GetRootLayer().identifier)

# Create PointInstancer
pi = UsdGeom.PointInstancer.Define(stage, "/World/Scatter")
# Create prototypes container
prototypes_prim = UsdGeom.Scope.Define(stage, pi.GetPath().AppendChild("Prototypes"))
# Reference the CubeBox_A04_26cm asset to use as a prototype
box = stage.DefinePrim(prototypes_prim.GetPath().AppendChild("CubeBox_A04_26cm"))
box_asset_path = stage_path.parent.parent / "src_assets" / "Assets" / "Components" / "CubeBox_A04_26cm" / "CubeBox_A04_26cm.usd"
box.GetReferences().AddReference(str(box_asset_path))
# Reference the BlockPallet_A07 asset to use as a prototype
pallet = stage.DefinePrim(prototypes_prim.GetPath().AppendChild("BlockPallet_A07"))
pallet_asset_path = stage_path.parent.parent / "src_assets" / "Assets" / "Components" / "BlockPallet_A07" / "BlockPallet_A07.usd"
pallet.GetReferences().AddReference(str(pallet_asset_path))

# Fill in PointInstancer with exported data.
# Required properties: prototypes, protoIndices, positions 
proto_rel = pi.CreatePrototypesRel()
proto_rel.SetTargets([
    box.GetPath(),
    pallet.GetPath()
])
pi.CreatePositionsAttr(export_data['positions'])
pi.CreateProtoIndicesAttr(export_data['proto_ids'])
pi.CreateOrientationsAttr([Gf.Quath(*vector) for vector in export_data['orientations']])

prototypes_prim.GetPrim().SetSpecifier(Sdf.SpecifierOver)

stage.Save()
