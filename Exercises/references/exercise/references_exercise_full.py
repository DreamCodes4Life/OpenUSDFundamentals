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


asset_library = Path(__file__).parent.parent.parent / "lib" / "assets"
working_dir = Path(__file__).parent
skyscraperA_file = asset_library / "envir" / "city" / "skyscraperA" / "skyscraperA.usd"
skyscraperA_relpath = os.path.relpath(skyscraperA_file, working_dir)
# Use forward slashes for file URIs for better cross-platform portability.
skyscraperA_relpath = Path(skyscraperA_relpath).as_posix()
skyscraperE_file = asset_library / "envir" / "city" / "skyscraperE" / "skyscraperE.usd"
skyscraperE_relpath = os.path.relpath(skyscraperE_file, working_dir)
skyscraperE_relpath = Path(skyscraperE_relpath).as_posix()
stage = Usd.Stage.CreateNew(str(working_dir / "city.usda"))
UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.centimeters)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

UsdGeom.Xform.Define(stage, "/World")
skyscraper_01 = UsdGeom.Xform.Define(stage, "/World/skyscraperA_01")
skyscraper_01.GetPrim().GetReferences().AddReference(skyscraperA_relpath)
skyscraper_02 = UsdGeom.Xform.Define(stage, "/World/skyscraperA_02")
skyscraper_02.GetPrim().GetReferences().AddReference(skyscraperA_relpath)
skyscraper_02_xformapi = UsdGeom.XformCommonAPI(skyscraper_02)
skyscraper_02_xformapi.SetTranslate(Gf.Vec3d(180, 0, 0))
skyscraper_03 = UsdGeom.Xform.Define(stage, "/World/skyscraperE_01")
skyscraper_03.GetPrim().GetReferences().AddReference(skyscraperE_relpath)
skyscraper_03_xformapi = UsdGeom.XformCommonAPI(skyscraper_03)
skyscraper_03_xformapi.SetTranslate(Gf.Vec3d(340, 0, 0))

stage.Save()

