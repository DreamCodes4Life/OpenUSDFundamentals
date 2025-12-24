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

from pxr import Usd

working_dir = Path(__file__).parent

stage: Usd.Stage = Usd.Stage.Open(str(working_dir / "lrg_bldgF.usd"))
default_prim: Usd.Prim = stage.GetDefaultPrim()
# Hard-coded, but by convention of our asset structure we can trust that the default
# prim has a Looks scope. 
looks_prim: Usd.Prim = stage.GetPrimAtPath(default_prim.GetPath().AppendChild("Looks"))
vsets: Usd.VariantSets = looks_prim.GetVariantSets()
# Loop through all of the variant sets defined on the Looks prim.
# Again relying on a convention of our custom asset structure that
# artists are define shading variant sets on the Looks prim.
for vset_name in vsets.GetNames():
    vset: Usd.VariantSet = vsets.GetVariantSet(vset_name)
    variants = vset.GetVariantNames()
    default = vset.GetVariantSelection()
    # ADD CODE BELOW HERE
    # vvvvvvvvvvvvvvvvvvv

    # [...]

    # ^^^^^^^^^^^^^^^^^^^^
    # ADD CODE ABOVE HERE

stage.Save()