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
import random

from pxr import Sdf, Usd, UsdGeom

accent_choices = [(0.3372549, 0.7372549, 0.6), (0.14835148, 0.44579056, 0.74917495), 
                  (0.8151815, 0.76243955, 0.46005294), (0.81166536, 0.46005294, 0.8151815)]

working_dir = Path(__file__).parent

stage: Usd.Stage = Usd.Stage.Open(str(working_dir / "city_blockA.usd"))
shading_layer_path = "./contents/shading.usd"
shading_layer = Sdf.Layer.FindOrOpen(str(working_dir / shading_layer_path))
with Usd.EditContext(stage, shading_layer):
    print("Setting building shading variations...")
    # ADD CODE BELOW HERE
    # vvvvvvvvvvvvvvvvvvv

    # [...]

    # ^^^^^^^^^^^^^^^^^^^^
    # ADD CODE ABOVE HERE

stage.Save()