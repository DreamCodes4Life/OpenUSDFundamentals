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

from pxr import Usd, UsdGeom, Gf

working_dir = Path(__file__).parent
stage = Usd.Stage.CreateNew(str(working_dir / "city.usda"))
UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.centimeters)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

UsdGeom.Xform.Define(stage, "/World")
xform = UsdGeom.Xform.Define(stage, "/World/sm_bldgF_01")
xform.GetPrim().GetPayloads().AddPayload("./sm_bldgF.usd")
xform = UsdGeom.Xform.Define(stage, "/World/sm_bldgF_02")
xform.GetPrim().GetPayloads().AddPayload("./sm_bldgF.usd")
xform_api = UsdGeom.XformCommonAPI(xform)
xform_api.SetTranslate(Gf.Vec3d(180, 0, 0))
xform = UsdGeom.Xform.Define(stage, "/World/sm_bldgF_03")
xform.GetPrim().GetPayloads().AddPayload("./sm_bldgF.usd")
xform_api = UsdGeom.XformCommonAPI(xform)
xform_api.SetTranslate(Gf.Vec3d(340, 0, 0))

stage.Save()
