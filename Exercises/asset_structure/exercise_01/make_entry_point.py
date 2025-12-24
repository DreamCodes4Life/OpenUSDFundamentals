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

from pxr import Usd, UsdGeom


working_dir = Path(__file__).parent

stage = Usd.Stage.Open(str(working_dir / "export.usd"))
# Get all existing root prims
root_prims = stage.GetPseudoRoot().GetChildren()
# Create the entry point print. 
# We use the namespace `/World` by convention.
world_prim = UsdGeom.Xform.Define(stage, "/World").GetPrim()
# Set the default prim for referencing and payloading.
stage.SetDefaultPrim(world_prim)

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

# [...]

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE

stage.GetRootLayer().Export(str(working_dir / "lrg_bldgF.usd"), args={"format":"usda"})