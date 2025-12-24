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

from pxr import Sdf, Usd, UsdGeom, UsdShade

material_data = {
    "materials": {
        "door": {"diffuseColor": (0.3882353, 0.4, 0.44705883), "roughness": 1.0, "metallic": 1.0},
        "window": {"diffuseColor": (0.7372549, 0.8862745, 1), "roughness": 1.0, "metallic": 1.0},
        "material_defaultMat": {"diffuseColor": (0.764151, 0.764151, 0.764151), "roughness": 1.0, "metallic": 1.0},
        "border": {"diffuseColor": (0.56078434, 0.5686275, 0.6), "roughness": 1.0, "metallic": 1.0},
        "roof": {"diffuseColor": (0.3372549, 0.7372549, 0.6), "roughness": 1.0, "metallic": 1.0},
    },
    "assignments": {
        "large_buildingF": {
            "subsets": {
                "door": "door",
                "window":"window",
                "subset_defaultMat": "material_defaultMat",
                "border": "border",
                "roof": "roof"
            },
            "mesh_mtl": None
        }
        
    }
}


working_dir = Path(__file__).parent

stage: Usd.Stage = Usd.Stage.Open(str(working_dir / "lrg_bldgF.usd"))
shading_layer_path = "./contents/shading.usd"

if (Path(working_dir) / shading_layer_path).exists() and shading_layer_path in stage.GetRootLayer().subLayerPaths:
    shading_layer = Sdf.Layer.FindOrOpen(str(working_dir /shading_layer_path))
else:
    shading_layer = Sdf.Layer.CreateNew(str(working_dir / shading_layer_path), args={"format": "usda"})
    # prepend the shading layer because we want it to be stronger than geometry layer.
    stage.GetRootLayer().subLayerPaths.insert(0, shading_layer_path)

with Usd.EditContext(stage, shading_layer):
    # Export/Define all of the materials
    default_prim = stage.GetDefaultPrim()
    looks_scope = UsdGeom.Scope.Define(stage, default_prim.GetPath().AppendChild("Looks"))
    looks_path = looks_scope.GetPath()
    for mtl_name, mtl_props in material_data["materials"].items():
        mtl_path = looks_path.AppendChild(mtl_name)
        mtl_prim = UsdShade.Material.Define(stage, mtl_path)
        shader = UsdShade.Shader.Define(stage, mtl_path.AppendPath("Shader"))
        shader.CreateIdAttr("UsdPreviewSurface")
        shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(mtl_props["diffuseColor"])
        shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(mtl_props["roughness"])
        shader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(mtl_props["metallic"])
        mtl_prim.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")
        mtl_prim.CreateDisplacementOutput().ConnectToSource(shader.ConnectableAPI(), "displacement")
        # Store the mtl_prim for material binding later
        material_data["materials"][mtl_name]["mtl_prim"] = mtl_prim

    # Bind the materials
    for prim in stage.Traverse():
        # It would be more robust to use SdfPath to uniquely identify the meshes for
        # assignment because multiple meshes with the same name could exist in the scenegraph.
        if prim.IsA(UsdGeom.Mesh) and prim.GetName() in material_data["assignments"]:
            mesh_info = material_data["assignments"][prim.GetName()]
            if mesh_info["mesh_mtl"] is not None:
                # TODO: Assign material to mesh
                pass
            for subset_name, mtl_name in mesh_info["subsets"].items():
                subset_prim = prim.GetChild(subset_name)
                binding_api = UsdShade.MaterialBindingAPI.Apply(subset_prim)
                binding_api.Bind(material_data["materials"][mtl_name]["mtl_prim"])

stage.Save()