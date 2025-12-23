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

import os
from pathlib import Path

from pxr import Usd, UsdGeom, Sdf


working_dir = Path(__file__).parent
side_streets = ["road_straight_59", "road_straight_34", "road_straight_28", "road_straight_27"]

asset_stage = Usd.Stage.Open(str(working_dir / "main_street.usd"))
class_prim = asset_stage.CreateClassPrim("/_osm_street_data")
max_speed_attr = class_prim.CreateAttribute("osm:street:maxspeed", Sdf.ValueTypeNames.Int, custom=True)
max_speed_attr.Set(30)
for prim in asset_stage.Traverse():
    if prim.IsA(UsdGeom.Mesh) and prim.GetName().startswith("road_") and not "Barrier" in prim.GetName():
        prim.GetSpecializes().AddSpecialize(class_prim.GetPath())
        if prim.GetName() in side_streets:
            prim.GetAttribute("osm:street:maxspeed").Set(20)


asset_stage.Save()


scenario2 = Usd.Stage.Open(str(working_dir / "scenario_02.usd"))
class_prim = scenario2.OverridePrim("/_osm_street_data")
max_speed_attr = class_prim.CreateAttribute("osm:street:maxspeed", Sdf.ValueTypeNames.Int, custom=True)
max_speed_attr.Set(40)
scenario2.Save()
