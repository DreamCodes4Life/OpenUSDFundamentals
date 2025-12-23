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

from pxr import Usd, UsdLux, UsdShade, Sdf

working_dir = Path(__file__).parent
asset_stage = Usd.Stage.Open(str(working_dir / "street_lamp_dbl.usd"))
class_prim = asset_stage.CreateClassPrim("/_street_lamp_dbl")
root = asset_stage.GetDefaultPrim()
root.GetInherits().AddInherit(class_prim.GetPath())
asset_stage.Save()

scenario2 = Usd.Stage.Open(str(working_dir / "scenario_02.usd"))
class_prim = scenario2.OverridePrim("/_street_lamp_dbl")
light_prim = scenario2.OverridePrim(class_prim.GetPath().AppendPath("Lights/sphere_light_01"))
light = UsdLux.LightAPI(light_prim)
light.CreateColorAttr((0.5, 0.4, 0.1))
light_prim = scenario2.OverridePrim(class_prim.GetPath().AppendPath("Lights/sphere_light_02"))
light = UsdLux.LightAPI(light_prim)
light.CreateColorAttr((0.5, 0.4, 0.1))
shader_prim = scenario2.OverridePrim(class_prim.GetPath().AppendPath("Looks/light/light"))
shader = UsdShade.Shader(shader_prim)
shader.CreateInput("emissiveColor", Sdf.ValueTypeNames.Color3f).Set((0.5, 0.4, 0.1))

scenario2.Save()
