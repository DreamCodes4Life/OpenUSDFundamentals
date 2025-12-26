<img width="1458" height="442" alt="image" src="https://github.com/user-attachments/assets/cb3be4e7-cf02-4dfc-820d-7594be455aae" />

🔗 [Exam Guide](https://nvdam.widen.net/s/6kxsqcsrrw/ncp-openusd-development-study-guide)
🔗 [Dev Guide](https://docs.omniverse.nvidia.com/dev-guide/latest/programmer_ref/usd.html)



# 1) Composition: Exam Weight 23%

<p align="left">
  <strong>Authoring, design with, or debugging composition arcs. A developer needs to know all of the composition arcs, how they
work, and when and when it is appropriate to use each. The developer needs to be able to debug complex LIVRPS scenarios</strong>
</p>

🔗 [More info](https://openusd.org/release/glossary.html#liverps-strength-ordering)

---

##  1.0- Before you start, things you need to know

•	A **Prim** is a container for property data and nested PrimSpecs is the primary container object in USD. It can contain and order other prims or hold different kinds of data. They are composed of prim specs and property spec.

•	**PrimSpec** is a container for property data and nested PrimSpecs.

•	Composition arcs can only be applied on PrimSpecs

•	A **PrimStack** is a list of PrimSpecs that contribute opinions for a composed prim’s metadata.

•	A **primvar** is a special attribute that a renderer associates with a geometric primitive, and can vary (interpolate) the value of the attribute over the surface/volume of the primitive

•	Composition is cached, value resolution is not

•	Composition is internally multi-threaded, value resolution is meant to be client multi-threaded. USD’s primary guidance for clients wishing to maximize USD’s performance on multi-core systems is to perform as much simultaneous value resolution and data extraction as possible

•	Composition rules vary by composition arc, value resolution rules vary by metadatum.

•	An **index**, also referred to as a PrimIndex, is the result of composition. A prim’s index contains an ordered (from strongest to weakest) list of “Nodes”. All of the queries on USD classes except for stage-level metadata rely on prim indices to perform value resolution.

•	A **[primvar](https://openusd.org/release/glossary.html#usdglossary-primvar)** (primitive variable) is a special kind of attribute that can vary and interpolate across a geometric primitive. You work with primvars through UsdGeomImageable and UsdGeomPrimvar. Review its **[class](https://openusd.org/release/api/class_usd_geom_primvar.html)**

##  1.1- Creating Composition Arcs

**Composition arcs** are the operators that allow **USD (Universal Scene Description)** to combine multiple layers of scene description in specific ways.

They define **how opinions are discovered, ordered, and resolved** across multiple files and layers.

---

##  1.2- The 7 Composition Arc Types (LIVERPS)

Composition arcs are evaluated according to **strength ordering** (from weakest → strongest).

| Order | Arc Type | Purpose |
|-----|---------|--------|
| L | **Local (Layers)** | Local changes |
| I | **Inherit** | Share properties from a base prim |
| V | **VariantSet** | Enable configuration switching |
| E | **Relocate** | Move prim paths |
| R | **Reference** | Bring in external USD layers |
| P | **Payload** | Lazy-load external content |
| S | **Specialize** | Stronger form of inheritance |

> **Mnemonic:** **LIVERPS** — the strength ordering of composition arcs

---

### 1.2.1 - Sublayer (Local)

**Sublayer** is a special composition mechanism:

- It **does not support prim name changes**
- It applies to **all sublayers in the root layer’s LayerStack**
- Direct opinions from *every sublayer* are consulted
- Commonly used for **shot, sequence, and asset assembly**

This makes sublayers ideal for **non-destructive layering** of work from multiple departments.

---
The following example shows how a **shot** composes multiple layers and includes an entire **sequence**, which itself is composed of additional layers.

##### ⭐ Example: Shot → Sequence Composition

<table>
<tr>
<th align="left">shot.usd</th>
<th align="left">sequence.usd</th>
</tr>
<tr>
    
<td valign="top">
    
```usda
#usda 1.0
(
    subLayers = [
        @shotFX.usd@,
        @shotAnimationBake.usd@,
        @sequence.usd@
    ]
)
```
</td> 
<td valign="top">

```usda
#usda 1.0
(
    subLayers = [
        @sequenceFX.usd@,
        @sequenceLayout.usd@,
        @sequenceDressing.usd@
    ]
)
```
</td>
</table>

Bellow is an example to introduce the concept of Flattering, we are running this script from the script editor in Omniverse, with the shot.usd stage opened. Each of the referenced layers has only an xform in their stages. You can also use the flatten option in the Layer's tab

##### 🐍 Example Flattering the previous Example
---
<table>
  <tr>
    <th align="left">flattenShotUSD.py</th>
    <th align="left">shot_flattened.py</th>
  </tr>
  <tr>
    <td valign="top">
  
```usda
from pxr import Usd
import os
import omni.usd

# Get the currently open stage
stage = omni.usd.get_context().get_stage()
if not stage:
    raise RuntimeError("No stage is currently open")

# Get the root layer of the stage
root_layer = stage.GetRootLayer()

# Resolve the layer path
input_path = root_layer.realPath or root_layer.identifier
if not input_path:
    raise RuntimeError("Unable to resolve root layer path")

# Build output path in the same folder
folder = os.path.dirname(input_path)
base, ext = os.path.splitext(os.path.basename(input_path))
output_path = os.path.join(folder, f"{base}_flattened{ext}")

# Flatten the composed stage
flattened_layer = stage.Flatten()

# Export flattened layer
if not flattened_layer.Export(output_path):
    raise RuntimeError("Failed to export flattened USD")

print(f"✅ Flattened stage saved to:\n{output_path}")

```
  </td > 
    <td valign="top">
  
```usda
#usda 1.0
(

    doc = """Generated from Composed Stage of root layer F:\\ISAACSIM\\OPEN_USD_COURSE\\1_Composition\\shot.usd
"""
    endTimeCode = 0
    startTimeCode = -0.4
    timeCodesPerSecond = 24
)

def Xform "World"
{
    def Xform "Dressing"
    {
        quatd xformOp:orient = (1, 0, 0, 0)
        double3 xformOp:scale = (1, 1, 1)
        double3 xformOp:translate = (0, 0, 0)
        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:orient", "xformOp:scale"]
    }

    def Xform "Layout"
    {
        quatd xformOp:orient = (1, 0, 0, 0)
        double3 xformOp:scale = (1, 1, 1)
        double3 xformOp:translate = (0, 0, 0)
        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:orient", "xformOp:scale"]
    }

    def Xform "FX"
    {
        quatd xformOp:orient = (1, 0, 0, 0)
        double3 xformOp:scale = (1, 1, 1)
        double3 xformOp:translate = (0, 0, 0)
        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:orient", "xformOp:scale"]
    }

    def Xform "shotAnimationBake"
    {
        quatd xformOp:orient = (1, 0, 0, 0)
        double3 xformOp:scale = (1, 1, 1)
        double3 xformOp:translate = (0, 0, 0)
        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:orient", "xformOp:scale"]
    }

    def Xform "shotFX"
    {
        quatd xformOp:orient = (1, 0, 0, 0)
        double3 xformOp:scale = (1, 1, 1)
        double3 xformOp:translate = (0, 0, 0)
        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:orient", "xformOp:scale"]
    }
}

```
  </td > 
</table>


In the next example, please note that your FPS will affect the real time.

#### <ins>Layer Offsets for TimeSamples</ins>

**Layer offsets** allow TimeSamples to be **shifted and scaled** when a layer is brought in via **Sublayers or References**.

They are commonly used to:
- Retime animation clips
- Reuse animation data non-destructively
- Align animation in time without modifying the source layer

##### ⭐ Example Time Offset and Scale
---
<table>
  <tr>
    <th align="left">example.usd</th>
    <th align="left">notes</th>
  </tr>
  <tr>
    <td>
  
```usda
#usda 1.0
(
    subLayers = [
        @./someAnimation.usd@ (offset = 10; scale = 0.5)
    ]
)
```
  </td> 
  <td>
    
```usda
This USD will resolve as next:
A timesample of 30 in the someAnimation will be
resolved here at: 30*0.5 + 10 = 25.
Layer offsets cannot vary themselves over time
```
  </td> 
</table>

#### <ins>LayerStack:</ins> 
The ordered set of layers resulting from the recursive gathering of all SubLayers of a Layer, plus the layer itself as first and strongest.

##### ⭐ Example "TimeCodes Scaled to Real Time"
---
<table>
  <tr>
    <th align="left">example.usd</th>
    <th align="left">notes</th>
  </tr>
  <tr>
    <td>
  
```usda
#usda 1.0
(
    timeCodesPerSecond = 24
    framesPerSecond = 12
    endTimeCode = 240
    startTimeCode = 1
)

def Xform "Asset"
{
    def Sphere "Sphere"
    {
        double3 xformOp:translate.timeSamples = {
            1: (0, 5.0, 0),
            240: (0, -5.0, 0),
        }
        uniform token[] xformOpOrder = ["xformOp:translate"]
    }
}

```
  </td> 
  <td>
    
```usda
TimeCode 240 corresponds to 10 seconds of real time

If the left example layer was referenced into another
layer that specified a timeCodesPerSecond value of 48
the TimeSample at TimeCode 240 would be scaled to TimeCode
480 to ensure that the translation still occurs at 10
seconds of real time.

If the left example layer specified a framesPerSecond
of 12, this would not change the scaling of the TimeSample
at TimeCode 240, and instead change the playback rate in a
playback device to march forward by two TimeCodes for each
consecutive rendered frame, which will be held for 1/12 of
a second.
```
</td> 
</table>

##### 🧠 [Exercise 1 (SubLayers)](https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/sublayers/working-with-sublayers.html)

- [Files](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/sublayers)

### 1.2.2 - Inherit

Inherits is a composition arc that addresses the problem of adding a single, non-destructive edit (override) that can affect a whole class of distinct objects on a stage. Inherits acts as a non-destructive “broadcast” operator that applies opinions authored on one prim to every other prim that inherits the “source” prim; not only do property opinions broadcast over inherits arcs - all scene description, hierarchically from the source, inherits. 

🔗 [More info]([https://openusd.org/release/glossary.html#liverps-strength-ordering](https://openusd.org/release/glossary.html#usdglossary-instancing))

##### ⭐ Example "TimeCodes Scaled to Real Time"
---
<table>
  <tr>
    <th align="left">Trees.usd <br>demonstrating inherits</th>
    <th align="left">Forest.usd <br>demonstrating inherits propagation through references</th>
    <th align="left">Instanceable Trees</th>
  </tr>
  <tr>
    <td valign="top">
  
```usda
#usda 1.0

class Xform "_class_Tree"
{
    def Mesh "Trunk"
    {
        color3f[] primvars:displayColor = [(.8, .8, .2)]
    }

    def Mesh "Leaves"
    {
        color3f[] primvars:displayColor = [(0, 1, 0)]
    }
}

def "TreeA" (
    inherits = </_class_Tree>
)
{
}

def "TreeB" (
    inherits = </_class_Tree>
)
{
    over "Leaves"
    {
        color3f[] primvars:displayColor = [(0.8, 1, 0)]
    }
}


```
  </td> 
  <td valign="top">
    
```usda
#usda 1.0

# A new prim, of the same name as the original inherits target,
providing new overrides

class "_class_Tree"
{
    token size = "small"

    # It's autumn in California
    over "Leaves"
    {
        color3f[] primvars:displayColor = [(1.0, .1, .1)]
    }
}

# TreeB_1 still inherits from _class_Tree because its
referent does
def "TreeB_1" (
    references = @./Trees.usd@</TreeB>
)
{
}


```
</td> 
  <td valign="top">
    
```usda
#usda 1.0

class Xform "_class_Tree"
{
    def Mesh "Trunk"
    {
        color3f[] primvars:displayColor = [(.8, .8, .2)]
    }

    def Mesh "Leaves"
    {
        color3f[] primvars:displayColor = [(0, 1, 0)]
    }
}

def "TreeA" (
    inherits = </_class_Tree>
    instanceable = true
)
{
}

def "TreeB" (
    inherits = </_class_Tree>
    instanceable = true
)
{
    over "Leaves"
    {
        color3f[] primvars:displayColor = [(0.8, 1, 0)]
    }
}
```
</td> 
</table>

A prim can inherit from any prim that is neither a descendant nor ancestor of itself, regardless of the prim’s specifier or type.

The key difference between references and inherits is that references fully encapsulate their targets, and therefore “disappear” when composed through another layer of referencing, whereas the relationship between inheritors and their inherits target remains “live” through arbitrary levels of referencing. 

#### <ins>Instancing</ins> 

Instancing in USD is a feature that allows many instances of “the same” object to share the same representation (composed prims) on a UsdStage. Instances can be overridden in stronger layers, so it is possible to “break” an instance when necessary, if it must be uniquified.

Instancing in USD is a feature that allows many instances of “the same” object to share the same representation (composed prims) on a UsdStage. In exchange for this sharing of representation (which provides speed and memory benefits both for the USD core and, generally, for clients processing the UsdStage), we give up the ability to uniquely override opinions on prims beneath the “instance root”, although it is possible to override opinions that will affect all instances’ views of the data. 

In the next example, we create a class _Class_Cube_Red, then three cubes are instances of that class, the first two have modified position, the second has change opinion to a blue material, but is weaker so still will be red, the third is the same but this time is stronger, so the third cube will be blue without modifying the instance status.

##### ⭐ Example "Instancing a red cube and change opinion in instances"

<table>
    <td valign="top">
  
```usda
#usda 1.0

def Xform "World" (
    prepend apiSchemas = ["MaterialBindingAPI"]
)
{
    rel material:binding = </World/Looks/OmniPBR_Blue> (
        bindMaterialAs = "weakerThanDescendants"
    )

    class Scope "_Class_Cube_Red"
    {
        def Mesh "Cube" (
            prepend apiSchemas = ["MaterialBindingAPI"]
        )
        {
            float3[] extent = [(-0.5, -0.5, -0.5), (0.5, 0.5, 0.5)]
            int[] faceVertexCounts = [4, 4, 4, 4, 4, 4]
            int[] faceVertexIndices = [0, 1, 3, 2, 4, 6, 7, 5, 6, 2, 3, 7, 4, 5, 1, 0, 4, 0, 2, 6, 5, 7, 3, 1]
            rel material:binding = </World/_Class_Cube_Red/Looks/OmniPBR_Red> (
                bindMaterialAs = "weakerThanDescendants"
            )
            normal3f[] normals = [(0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, -1, 0), (0, -1, 0), (0, -1, 0), (0, -1, 0), (-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0)] (
                interpolation = "faceVarying"
            )
            point3f[] points = [(-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (-0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5)]
            texCoord2f[] primvars:st = [(0, 0), (1, 0), (1, 1), (0, 1), (1, 0), (1, 1), (0, 1), (0, 0), (0, 1), (0, 0), (1, 0), (1, 1), (0, 0), (1, 0), (1, 1), (0, 1), (0, 0), (1, 0), (1, 1), (0, 1), (1, 0), (1, 1), (0, 1), (0, 0)] (
                interpolation = "faceVarying"
            )
            uniform token subdivisionScheme = "none"
            quatd xformOp:orient = (1, 0, 0, 0)
            double3 xformOp:scale = (1, 1, 1)
            double3 xformOp:translate = (0, 1, 1)
            uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:orient", "xformOp:scale"]
        }

        def Scope "Looks"
        {
            def Material "OmniPBR_Red"
            {
                token outputs:mdl:displacement.connect = </World/_Class_Cube_Red/Looks/OmniPBR_Red/Shader.outputs:out>
                token outputs:mdl:surface.connect = </World/_Class_Cube_Red/Looks/OmniPBR_Red/Shader.outputs:out>
                token outputs:mdl:volume.connect = </World/_Class_Cube_Red/Looks/OmniPBR_Red/Shader.outputs:out>

                def Shader "Shader"
                {
                    uniform token info:implementationSource = "sourceAsset"
                    uniform asset info:mdl:sourceAsset = @OmniPBR.mdl@
                    uniform token info:mdl:sourceAsset:subIdentifier = "OmniPBR"
                    color3f inputs:diffuse_tint = (0.90759075, 0.12366932, 0.01797209)
                    token outputs:out (
                        renderType = "material"
                    )
                }
            }
        }
    }

    def Xform "Cube_01" (
        inherits = </World/_Class_Cube_Red>
        instanceable = true
    )
    {
        quatf xformOp:orient = (1, 0, 0, 0)
        float3 xformOp:scale = (1, 1, 1)
        double3 xformOp:translate = (1.6772258843990702, 0, 0)
        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:orient", "xformOp:scale"]
    }

    def Xform "Cube_02" (
        prepend apiSchemas = ["MaterialBindingAPI"]
        inherits = </World/_Class_Cube_Red>
        instanceable = true
    )
    {
        rel material:binding = </World/Looks/OmniPBR_Blue> (
            bindMaterialAs = "strongerThanDescendants"
        )
        quatf xformOp:orient = (1, 0, 0, 0)
        float3 xformOp:scale = (1, 1, 1)
        double3 xformOp:translate = (0, 1.8461749821880287, 0)
        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:orient", "xformOp:scale"]
    }

    def Xform "Cube_03" (
        prepend apiSchemas = ["MaterialBindingAPI"]
        inherits = </World/_Class_Cube_Red>
        instanceable = true
    )
    {
        rel material:binding = </World/Looks/OmniPBR_Blue> (
            bindMaterialAs = "weakerThanDescendants"
        )
    }

    def Scope "Looks"
    {
        def Material "OmniPBR_Yellow"
        {
            token outputs:mdl:displacement.connect = </World/Looks/OmniPBR_Yellow/Shader.outputs:out>
            token outputs:mdl:surface.connect = </World/Looks/OmniPBR_Yellow/Shader.outputs:out>
            token outputs:mdl:volume.connect = </World/Looks/OmniPBR_Yellow/Shader.outputs:out>

            def Shader "Shader"
            {
                uniform token info:implementationSource = "sourceAsset"
                uniform asset info:mdl:sourceAsset = @OmniPBR.mdl@
                uniform token info:mdl:sourceAsset:subIdentifier = "OmniPBR"
                color3f inputs:diffuse_tint = (0.882679, 0.90759075, 0.06889302)
                token outputs:out (
                    renderType = "material"
                )
            }
        }

        def Material "OmniPBR_Blue"
        {
            token outputs:mdl:displacement.connect = </World/Looks/OmniPBR_Blue/Shader.outputs:out>
            token outputs:mdl:surface.connect = </World/Looks/OmniPBR_Blue/Shader.outputs:out>
            token outputs:mdl:volume.connect = </World/Looks/OmniPBR_Blue/Shader.outputs:out>

            def Shader "Shader"
            {
                uniform token info:implementationSource = "sourceAsset"
                uniform asset info:mdl:sourceAsset = @OmniPBR.mdl@
                uniform token info:mdl:sourceAsset:subIdentifier = "OmniPBR"
                color3f inputs:diffuse_tint = (0.029408854, 0.08059826, 0.8910891)
                token outputs:out (
                    renderType = "material"
                )
            }
        }
    }
}

```
  </td >   
</table>

<img width="1955" height="1108" alt="image" src="https://github.com/user-attachments/assets/34141fad-0f83-432a-ae3a-74fff5f77bf7" />

##### ⭐ Example "Adding variants to the previous example"
---
<table>
    <td valign="top">
  
```usda
def Xform "World"
{
    class Scope "_Class_Cube_Red"
    {
        def Mesh "Cube" (
            prepend apiSchemas = ["MaterialBindingAPI"]
            variants = {
                string ChangeColor = "Variant"
            }
            prepend variantSets = "ChangeColor"
        )
        {
            float3[] extent = [(-0.5, -0.5, -0.5), (0.5, 0.5, 0.5)]
            int[] faceVertexCounts = [4, 4, 4, 4, 4, 4]
            int[] faceVertexIndices = [0, 1, 3, 2, 4, 6, 7, 5, 6, 2, 3, 7, 4, 5, 1, 0, 4, 0, 2, 6, 5, 7, 3, 1]
            normal3f[] normals = [(0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, -1, 0), (0, -1, 0), (0, -1, 0), (0, -1, 0), (-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0)] (
                interpolation = "faceVarying"
            )
            point3f[] points = [(-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (-0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5)]
            texCoord2f[] primvars:st = [(0, 0), (1, 0), (1, 1), (0, 1), (1, 0), (1, 1), (0, 1), (0, 0), (0, 1), (0, 0), (1, 0), (1, 1), (0, 0), (1, 0), (1, 1), (0, 1), (0, 0), (1, 0), (1, 1), (0, 1), (1, 0), (1, 1), (0, 1), (0, 0)] (
                interpolation = "faceVarying"
            )
            uniform token subdivisionScheme = "none"
            quatd xformOp:orient = (1, 0, 0, 0)
            double3 xformOp:scale = (1, 1, 1)
            double3 xformOp:translate = (0, 1, 1)
            uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:orient", "xformOp:scale"]
            variantSet "ChangeColor" = {
                "Variant" (
                    prepend apiSchemas = ["MaterialBindingAPI"]
                    customData = {
                        string[] variantPrimPaths = ["."]
                    }
                ) {
                    rel material:binding = </World/Cube_01/Looks/OmniPBR_Yellow> (
                        bindMaterialAs = "weakerThanDescendants"
                    )

                }
                "Variant_1" (
                    prepend apiSchemas = ["MaterialBindingAPI"]
                    customData = {
                        string[] variantPrimPaths = ["."]
                    }
                ) {
                    rel material:binding = </World/Looks/OmniPBR_Blue> (
                        bindMaterialAs = "weakerThanDescendants"
                    )

                }
            }
        }

        def Scope "Looks"
        {
            def Material "OmniPBR_Red"
            {
                token outputs:mdl:displacement.connect = </World/_Class_Cube_Red/Looks/OmniPBR_Red/Shader.outputs:out>
                token outputs:mdl:surface.connect = </World/_Class_Cube_Red/Looks/OmniPBR_Red/Shader.outputs:out>
                token outputs:mdl:volume.connect = </World/_Class_Cube_Red/Looks/OmniPBR_Red/Shader.outputs:out>

                def Shader "Shader"
                {
                    uniform token info:implementationSource = "sourceAsset"
                    uniform asset info:mdl:sourceAsset = @OmniPBR.mdl@
                    uniform token info:mdl:sourceAsset:subIdentifier = "OmniPBR"
                    color3f inputs:diffuse_tint = (0.90759075, 0.12366932, 0.01797209)
                    token outputs:out (
                        renderType = "material"
                    )
                }
            }

            def Material "OmniPBR_Yellow"
            {
                token outputs:mdl:displacement.connect = </World/_Class_Cube_Red/Looks/OmniPBR_Yellow/Shader.outputs:out>
                token outputs:mdl:surface.connect = </World/_Class_Cube_Red/Looks/OmniPBR_Yellow/Shader.outputs:out>
                token outputs:mdl:volume.connect = </World/_Class_Cube_Red/Looks/OmniPBR_Yellow/Shader.outputs:out>
                custom uniform bool paused = 0 (
                    customData = {
                        bool nonpersistant = 1
                    }
                    hidden = true
                )

                def Shader "Shader"
                {
                    uniform token info:implementationSource = "sourceAsset"
                    uniform asset info:mdl:sourceAsset = @OmniPBR.mdl@
                    uniform token info:mdl:sourceAsset:subIdentifier = "OmniPBR"
                    color3f inputs:diffuse_tint = (0.882679, 0.90759075, 0.06889302)
                    token outputs:out (
                        renderType = "material"
                    )
                }
            }
        }
    }

    def Xform "Cube_01" (
        inherits = </World/_Class_Cube_Red>
        instanceable = true
    )
    {
        quatf xformOp:orient = (1, 0, 0, 0)
        float3 xformOp:scale = (1, 1, 1)
        double3 xformOp:translate = (1.6772258843990702, 0, 0)
        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:orient", "xformOp:scale"]
    }

    def Xform "Cube_02" (
        prepend apiSchemas = ["MaterialBindingAPI"]
        inherits = </World/_Class_Cube_Red>
        instanceable = true
    )
    {
        rel material:binding = </World/Looks/OmniPBR_Blue> (
            bindMaterialAs = "strongerThanDescendants"
        )
        quatf xformOp:orient = (1, 0, 0, 0)
        float3 xformOp:scale = (1, 1, 1)
        double3 xformOp:translate = (0, 1.8461749821880287, 0)
        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:orient", "xformOp:scale"]
    }

    def Xform "Cube_03" (
        prepend apiSchemas = ["MaterialBindingAPI"]
        inherits = </World/_Class_Cube_Red>
        instanceable = true
    )
    {
        rel material:binding = </World/Looks/OmniPBR_Blue> (
            bindMaterialAs = "weakerThanDescendants"
        )
    }

    def Xform "Cube_04" (
        inherits = </World/_Class_Cube_Red>
        instanceable = true
    )
    {
        color3f[] primvars:displayColor = [(0, 1, 0)] (
            interpolation = "constant"
        )
        uniform token purpose = "default"
        token visibility = "inherited"
        quatf xformOp:orient = (1, 0, 0, 0)
        float3 xformOp:scale = (1, 1, 1)
        double3 xformOp:translate = (1.4336037158412456, 1.6727603814796503, 0)
        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:orient", "xformOp:scale"]
    }

    def Cube "Cube_05" (
    )
    {
        float3[] extent = [(-0.5, -0.5, -0.5), (0.5, 0.5, 0.5)]
        color3f[] primvars:displayColor = [(0, 1, 0)] (
            interpolation = "constant"
        )
        double size = 1
        quatd xformOp:orient = (1, 0, 0, 0)
        double3 xformOp:scale = (1, 1, 1)
        double3 xformOp:translate = (3.2250553274445837, 0, 0)
        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:orient", "xformOp:scale"]
    }    

    def Scope "Looks"
    {
        def Material "OmniPBR_Yellow"
        {
            token outputs:mdl:displacement.connect = </World/Looks/OmniPBR_Yellow/Shader.outputs:out>
            token outputs:mdl:surface.connect = </World/Looks/OmniPBR_Yellow/Shader.outputs:out>
            token outputs:mdl:volume.connect = </World/Looks/OmniPBR_Yellow/Shader.outputs:out>

            def Shader "Shader"
            {
                uniform token info:implementationSource = "sourceAsset"
                uniform asset info:mdl:sourceAsset = @OmniPBR.mdl@
                uniform token info:mdl:sourceAsset:subIdentifier = "OmniPBR"
                color3f inputs:diffuse_tint = (0.882679, 0.90759075, 0.06889302)
                token outputs:out (
                    renderType = "material"
                )
            }
        }

        def Material "OmniPBR_Blue"
        {
            token outputs:mdl:displacement.connect = </World/Looks/OmniPBR_Blue/Shader.outputs:out>
            token outputs:mdl:surface.connect = </World/Looks/OmniPBR_Blue/Shader.outputs:out>
            token outputs:mdl:volume.connect = </World/Looks/OmniPBR_Blue/Shader.outputs:out>

            def Shader "Shader"
            {
                uniform token info:implementationSource = "sourceAsset"
                uniform asset info:mdl:sourceAsset = @OmniPBR.mdl@
                uniform token info:mdl:sourceAsset:subIdentifier = "OmniPBR"
                color3f inputs:diffuse_tint = (0.029408854, 0.08059826, 0.8910891)
                token outputs:out (
                    renderType = "material"
                )
            }
        }
    }
}

```
  </td >   
</table>

<img width="2116" height="976" alt="image" src="https://github.com/user-attachments/assets/33b8fda0-3d34-4409-8440-8215754cd8d5" />

🔗 [More info](https://openusd.org/release/glossary.html#usdglossary-instancing)

### 1.2.3 - VariantSets and Variants:

Apply the resolved variant selections to all VariantSets that affect the PrimSpec at path in the LayerStack, and iterate through the selected Variants on each VariantSet. For each target, recursively apply LIVERP evaluation on the targeted LayerStack - Note that the “S” is not present - we ignore Specializes arcs while recursing
A VariantSet is a composition arc that allows a content creator to package a discrete set of alternatives, between which a downstream consumer is able to non-destructively switch, or augment.

A variant can contain overriding opinions (for properties, metadata, and more), as well as any arbitrary scene description (entire child prim subtrees, etc). Variants can also include additional composition arcs.

##### ⭐ Example Simple VarianSet
---
<table>
  <tr>
    <th align="left">simpleVariantSet.usd</th>
    <th align="left">VariantSet with references</th>
  </tr>
  <tr>
    <td valign="top">
  
```usda
#usda 1.0

def Xform "Implicits" (
    append variantSets = "shapeVariant"
)
{
    variantSet "shapeVariant" = {
        "Capsule" {
            def Capsule "Pill"
            {
            }
        }
        "Cone" {
            def Cone "PartyHat"
            {
            }
        }
        "Cube" {
            def Cube "Box"
            {
            }
        }
        "Cylinder" {
            def Cylinder "Tube"
            {
            }
        }
        "Sphere" {
            def Sphere "Ball"
            {
            }
        }
    }
}

```
  </td > 
  <td valign="top">
    
```usda
over "Model" (
    prepend variantSets = "referenceVariantSet"
    variants = {
       string referenceVariantSet = "asset1"
    }
)
{
    variantSet "referenceVariantSet" = {
        "asset1" (
            prepend references = @Asset1.usda@
        ) {
        }
        "asset2" (
            prepend references = @Asset2.usda@
        ) {
        }
    }
}

```
  </td>   
</table>

#### <ins>Nested VariantSets</ins> 

VariantSets can be nested directly inside each other, on the same prim.

##### 🐍 Example Nested VarianSets (Python)
---
<table>
  <tr>
    <th align="left">nestedVariants.py</th>
  </tr>
  <tr>
    <td valign="top">
  
```usda
from pxr import Sdf, Usd
stage = Usd.Stage.CreateNew("nestedVariants.usd")
prim = stage.DefinePrim("/Employee")
title = prim.CreateAttribute("title", Sdf.ValueTypeNames.String)
variantSets = prim.GetVariantSets()

critters = [ "Bug", "Bear", "Dragon" ]
jobs = [ "Squasher", "Rider", "Trainer" ]

critterVS = variantSets.AppendVariantSet("critterVariant")
for critter in critters:
    critterVS.AppendVariant(critter)
    critterVS.SetVariantSelection(critter)
    with critterVS.GetVariantEditContext():
        # All edits now go "inside" the selected critter variant
        jobVS = variantSets.AppendVariantSet("jobVariant")
        for job in jobs:
            if (job != "Squasher" or critter == "Bug") and \
               (job != "Rider" or critter != "Bug") :
                jobVS.AppendVariant(job)
                jobVS.SetVariantSelection(job)
                with jobVS.GetVariantEditContext():
                    # Now edits *additionally* go inside the selected job variant
                    title.Set(critter + job)
stage.GetRootLayer().Save()
```
  </td > 
</table>

Basically we are making a variantSet and attribute depending on other varianSets

##### 🧠 [Exercise (Authoring Variants)](https://openusd.org/release/tut_authoring_variants.html)

##### 🐍 [i.e. (Add VariantSets in Python)](https://github.com/DreamCodes4Life/OpenUSDFundamentals/blob/main/03_CompositionBasics/07_addVariantSetAndVariants.py)  🐍 [i.e. (Add Multiple Variants in Python)](https://github.com/DreamCodes4Life/OpenUSDFundamentals/blob/main/03_CompositionBasics/08_addMoreVariants.py)  🐍 [i.e. (Edit VariantSets in Python)](https://github.com/DreamCodes4Life/OpenUSDFundamentals/blob/main/03_CompositionBasics/09_editVariants.py)


🔗 [More info](https://openusd.org/release/glossary.html#usdglossary-variant)

### 1.2.4 - R(E)locates: 
Relocates is a composition arc that maps a prim path defined in a remote LayerStack (i.e. across a composition arc) to a new path location in the local namespace (these paths can only be prim paths, not property paths).

##### ⭐ Example "Relocates"
---
<table>
  <tr>
    <th align="left">refLayer.usda</th>
    <th align="left">main.usda</th>
    <th align="left">flattened main.usda</th>
  </tr>
  <tr>
    <td valign="top">
  
```usda
def "PrimA" ()
{
    def "PrimAChild" ()
    {
        uniform string testString = "test"
        float childValue = 3.5
    }
}
```
  </td> 
  <td valign="top">
    
```usda
#usda 1.0
(
    relocates = {
        </MainPrim/PrimAChild> : </MainPrim/RenamedPrimAChild>
    }
)
def "MainPrim" (
    prepend references = @refLayer.usda@</PrimA>
)
{
    over RenamedPrimAChild
    {
        float childValue = 5.2
    }
}
```
</td> 
  <td valign="top">
    
```usda
def "MainPrim"
{
    def "RenamedPrimAChild"
    {
        float childValue = 5.2
        uniform string testString = "test"
    }
}
```
</td> 
</table>

- You cannot relocate a root prim.
- When a source path is relocated, that original source path is considered no longer valid in the current namespace. Any local opinions authored on a source path will generate a “invalid option at relocation source path” error.
- Relocates that would create invalid or conflicting namespace paths are not allowed

##### ⭐ Example "Relocates respect to composition strength ordering"
---
<table>
  <tr>
    <th align="left">main.usda <br>with added class and inherits</th>
    <th align="left">flattened main.usda <br>with inherits and relocates applied</th>
  </tr>
  <tr>
    <td valign="top">
  
```usda
#usda 1.0
(
    relocates = {
        </MainPrim/PrimAChild> : </MainPrim/RenamedPrimAChild>
    }
)

class "WorkClass"
{
    float childValue = 20.5
    uniform string testString = "from WorkClass"
}

def "MainPrim" (
    prepend references = @refLayer.usda@</PrimA>
)
{
    def "RenamedPrimAChild"
    (
        inherits = </WorkClass>
    )
    {
    }
}
```
  </td> 
  <td valign="top">
    
```usda
#usda 1.0
(
    relocates = {
        </MainPrim/PrimAChild> : </MainPrim/RenamedPrimAChild>
    }
)
def "MainPrim" (
    prepend references = @refLayer.usda@</PrimA>
)
{
    over RenamedPrimAChild
    {
        float childValue = 5.2
    }
}
```
</td> 
</table>

#### <ins>Relocates and inherits</ins> 

A relocated prim will still inherit the same opinions it would have had it not been relocated. This can result in some subtle composition behavior.

##### ⭐ Example "Relocates and composition strength ordering with inherits"

In the next flattened stage, /Model/Rig/LRig in model.usda has inherited from /ClassA/Rig/LRig even though it was relocated to /Model/Anim/LAnim in that layer, and does not inherit opinions from /ClassA/Anim/LAnim. However, note that /Model_1/Anim/LAnim in the root.usda layer does inherit from the layer’s /ClassA/Anim/LAnim.

---
<table>
  <tr>
    <th align="left">model.usda <br>with ClassA and Model that inherits from ClassA</th>
    <th align="left">root.usda</th>
    <th align="left">flattened root.usda/th>
  </tr>
  <tr>
    <td valign="top">
  
```usda
#usda 1.0
(
    relocates = {
        </Model/Rig/LRig>: </Model/Anim/LAnim>
    }
)

class "ClassA"
{
    def "Rig"
    {
        def "LRig"
        {
            uniform token modelClassALRig = "test"
        }
    }

    def "Anim"
    {
        def "LAnim"
        {
            uniform token modelClassALAnim = "test"
        }
    }
}

def "Model" (
    inherits = </ClassA>
)
{
}
```
  </td> 
  <td valign="top">
    
```usda
def "Model_1" (
    references = @./model.usda@</Model>
)
{
}

class "ClassA"
{
    def "Rig"
    {
        def "LRig"
        {
            uniform token rootClassALRig = "test"
        }
    }

    def "Anim"
    {
        def "LAnim"
        {
            uniform token rootClassALAnim = "test"
        }
    }
}
```
</td> 
  <td valign="top">
    
```usda
def "Model_1"
{
    def "Rig"
    {
    }

    def "Anim"
    {
        def "LAnim"
        {
            uniform token modelClassALRig = "test"
            uniform token rootClassALAnim = "test"
            uniform token rootClassALRig = "test"
        }
    }
}
```
</td> 
</table>

#### <ins>Relocates and ancestral arcs during composition</ins> 

One aspect of relocates and composition is that relocates will ignore all ancestral arcs except variant arcs when we build the PrimIndex for a prim. So, if you had a layer that relocates a prim to be the child of a prim with an ancestral inherits arc:

##### ⭐ Example "Layer with ancestral inherits and relocates"

Next with the relocates for /PrimA/Child to /PrimWithInherits/Child, the ancestral opinions from /ClassA/Child are ignored.

<table>
  <tr>
    <th align="left">layer.usd</th>
    <th align="left">flattened layer</th>
  </tr>
  <tr>
  <td valign="top">
    
```usda
#usda 1.0
(
    relocates = {
        </PrimA/Child>: </PrimWithInherits/Child>
    }
)

def "ClassA"
(
)
{
    def "Child"
    {
        uniform token testString = "from ClassA/Child"
        uniform token classAChildString = "test"
    }
}

def "RefPrim"
(
)
{
    def "Child"
    {
        uniform token testString = "from RefPrim/Child"
        uniform token refPrimChildString = "test"
    }
}

def "PrimA"
(
    prepend references = </RefPrim>
)
{
}


def "PrimWithInherits"
(
    inherits = </ClassA>
)
{
}
```
</td> 
  <td valign="top">
    
```usda
def "PrimWithInherits"
{
    def "Child"
    {
        uniform token refPrimChildString = "test"
        uniform token testString = "from RefPrim/Child"
    }
}
```
</td> 
</table>

##### ⭐ Example "Layer with ancestral variantSets and relocates"

Next we see as ancestral variant arcs will still compose with relocate

<table>
  <tr>
    <th align="left">layer.usd</th>
    <th align="left">flattened layer</th>
  </tr>
  <tr>
  <td valign="top">
    
```usda
#usda 1.0
(
    relocates = {
        </PrimA/Child>: </PrimWithInherits/Child>
    }
)

def "ClassA"
(
)
{
    def "Child"
    {
        uniform token testString = "from ClassA/Child"
        uniform token classAChildString = "test"
    }
}

def "RefPrim"
(
)
{
    def "Child"
    {
        uniform token testString = "from RefPrim/Child"
        uniform token refPrimChildString = "test"
    }
}

def "PrimA"
(
    prepend references = </RefPrim>
)
{
}


def "PrimWithInherits"
(
    # Removed inherits of ClassA
    # Added variantSet and selection with authored Child opinions
    variants = {
        string varSet = "Set1"
    }
    prepend variantSets = "varSet"
)
{
    variantSet "varSet" = {
        "Set1" ()
        {
            def "Child"
            {
                uniform token testString = "from varSet Child"
                uniform token varChildString = "test"
            }
        }
        "Set2" ()
        {
        }
    }
}
```
</td> 
  <td valign="top">
    
```usda
def "PrimWithInherits"
{
    def "Child"
    {
        uniform token refPrimChildString = "test"
        uniform token testString = "from varSet Child"
        uniform token varChildString = "test"
    }
}
```
</td> 
</table>

##### 🐍 [i.e. (Relocates in Python)](https://github.com/DreamCodes4Life/OpenUSDFundamentals/blob/main/03_CompositionBasics/10_relocateScript.py)

🔗 [More info](https://openusd.org/release/glossary.html#relocates)

### 1.2.5 - References

Resolve the References affecting the prim at path, and iterate through the resulting targets. For each target, recursively apply LIVERP evaluation on the targeted LayerStack - Note that the “S” is not present - we ignore Specializes arcs while recursing.

##### ⭐ Example "References"

<table>
  <tr>
    <th align="left">Marble.usd</th>
    <th align="left">MarbleCollection.usd</th>
    <th align="left">FlattenedMarbleCollection.usd</th>
  </tr>
  <tr>
  <td valign="top">
    
```usda
#usda 1.0
(
    defaultPrim = "Marble"
)

def Xform "Marble" (
    kind = "component"
)
{
    def Sphere "marble_geom"
    {
        color3f[] primvars:displayColor = [ (0, 1, 0) ]
    }
}
```
</td> 
  <td valign="top">
    
```usda
#usda 1.0

def Xform "MarbleCollection" (
    kind = "assembly"
)
{
    def "Marble_Green" (
            references = @Marble.usd@
        )
    {
        double3 xformOp:translate = (-10, 0, 0)
        uniform token[] xformOpOrder = [ "xformOp:translate" ]
    }

    def "Marble_Red" (
        references = @Marble.usd@
    )
    {
        double3 xformOp:translate = (5, 0, 0)
        uniform token[] xformOpOrder = [ "xformOp:translate" ]

        over "marble_geom"
        {
            color3f[] primvars:displayColor = [ (1, 0, 0) ]
        }
    }
}
```
</td> 
</td> 
  <td valign="top">
    
```usda
#usda 1.0

def Xform "MarbleCollection" (
    kind = "assembly"
)
{
    def Xform "Marble_Green" (
        kind = "component"
    )
    {
        double3 xformOp:translate = (-10, 0, 0)
        uniform token[] xformOpOrder = [ "xformOp:translate" ]

        def Sphere "marble_geom"
        {
            color3f[] primvars:displayColor = [ (0, 1, 0) ]
        }
    }

    def Xform "Marble_Red" (
        kind = "component"
    )
    {
        double3 xformOp:translate = (5, 0, 0)
        uniform token[] xformOpOrder = [ "xformOp:translate" ]

        def Sphere "marble_geom"
        {
            color3f[] primvars:displayColor = [ (1, 0, 0) ]
        }
    }
}
```
</td> 
</table>

References can target any prim in a LayerStack, excepting ancestors of the prim containing the reference

#### <ins>Relationship</ins> 

A Relationship is a “namespace pointer” that is robust in the face of composition arcs, which means that when you ask USD for a relationship’s targets, USD will perform all the necessary namespace-manipulations required to translate the authored target value into the scene-level namespace.

##### ⭐ Example "Relationship"

<table>
  <tr>
    <th align="left">Marble.usd</th>
  </tr>
  <tr>
  <td valign="top">
    
```usda
#usda 1.0
(
    defaultPrim = "Marble"
)

def Xform "Marble" (
    kind = "component"
)
{
    def Sphere "marble_geom"
    {
        rel material:binding = </Marble/GlassMaterial>
        color3f[] primvars:displayColor = [ (0, 1, 0) ]
    }

    def Material "GlassMaterial"
    {
        # Interface inputs, shading networks, etc.
    }
}
```
</td> 
</table>

##### ⭐ Example "Referencing sub-root prims"

<table>
  <tr>
    <th align="left">shot.usda</th>
    <th align="left">asset.usda</th>
  </tr>
  <tr>
  <td valign="top">
    
```usda
#usda 1.0

over "Class" 
{              
    over "B"    
    {                                       
        over "Model"
        {      
            int a = 3  
        }        
    }            
}              

over "A"                  
{                    
    over "B" (               
        # variant selection won't be used
        variants = {    
            string type = "b"  
        }              
    )                
    {                 
    }                            
}                             

def "ReferencedModel" (        
    references = @./asset.usda@</A/B/Model>
)                          
{                           
}                           
                          
```
</td> 
  <td valign="top">

```usda
#usda 1.0

 class "Class"
 {
 }

 def "A" (
    inherits = </Class>
 )
 {
     token purpose = "render"

     def "B" (
        variantSets = "type"
        variants = {
             string type = "a"
        }
     )
     {
         variantSet "type" = {
             "a" {
                 def "Model"
                 {
                     int a = 1
                 }
             }
             "b" {
                 def "Model"
                 {
                     int a = 2
                 }
             }
         }
     }
 }
```
</td> 
</table>

##### 🐍 [i.e. (Add Reference in Python)](https://github.com/DreamCodes4Life/OpenUSDFundamentals/blob/main/03_CompositionBasics/02_ReferenceExternalAsset.py)

🔗 [More info](https://openusd.org/release/glossary.html#usdglossary-references)

### 1.2.6 - Payloads

A Payload is a composition arc that is a special kind of a Reference. It is different from references primarily in:

  - The targets of References are always consumed greedily by the indexing algorithm that is used to open and build a Stage. When a Stage is opened with UsdStage::InitialLoadSet::LoadNone specified, Payload arcs are recorded, but not traversed. This behavior allows clients to manually construct a “working set” that is a subset of the whole scene, by loading just the bits of the scene that they require.

### 1.2.7 - Specializes

Specializes is a composition arc that allows a specialized prim to be continuously refined from a base prim, through unlimited levels of referencing.

##### ⭐ Example "Specializes"

<table>
  <tr>
    <th align="left">Robot.usd</th>
    <th align="left">RobotScene.usd</th>
  </tr>
  <tr>
  <td valign="top">
    
```usda
#usda 1.0

def Xform "Robot"
{
    def Scope "Materials"
    {
        def Material "Metal"
        {
            # Interface inputs drive shader parameters of the encapsulated
            # network. We are not showing the connections, nor how we encode
            # that the child Shader "Surface" is the primary output for the
            # material.
            float inputs:diffuseGain = 0
            float inputs:specularRoughness = 0

            def Shader "Surface"
            {
                asset info:id = @PxrSurface@
            }
        }

        def Material "CorrodedMetal" (
            specializes = </Robot/Materials/Metal>
        )
        {
            # specialize roughness...
            float inputs:specularRoughness = 0.2

            # Adding a pattern to drive Surface bump
            def Shader "Corrosion"
            {
                asset info:id = @PxrOSL@
                vector3f outputs:disp
            }

            over "Surface"
            {
                # Override that would connect specularBump to Corrosion
                # pattern's "outputs:disp" attribute
            }
        }
    }
}
```
</td> 
  <td valign="top">
    
```usda
#usda 1.0
def Xform "World"
{
    def Xform "Characters"
    {
        def "Rosie" (
            references = @./Robot.usd@</Robot>
        )
        {
            over "Materials"
            {
                over "Metal"
                {
                     float inputs:diffuseGain = 0.3
                     float inputs:specularRoughness = 0.1
                }
            }
        }
    }
}
```
</td> 
</table>

In the above example if you examine the flattened RobotScene.usd you will see the effect of specializes on the specialized /World/Characters/Rosie/Materials/CorrodedMetal prim: we overrode both diffuseGain and specularRoughness on the base Metal material, but only the diffuseGain propagates onto /World/Characters/Rosie/Materials/CorrodedMetal, because specularRoughness was already refined on the referenced /Robot/Materials/CorrodedMetal prim. This also demonstrates the difference between specializes and inherits: if you change the specializes arc to inherits in Robot.usd and recompose the scene, you will see that both diffuseGain and specularRoughness propagate onto /World/Characters/Rosie/Materials/CorrodedMetal.



# 2) Content Aggregation: Exam Weight 10%

<p align="left">
  <strong>Create modular, reusable components, leverage instancing (native and point) to optimize a scene, and apply different
strategies for overriding an instanced asset for efficient, optimized, and collaborative aggregation of assets (models) to build
large scenes.</strong>
</p>

##  2.0- Before you start, things you need to know

##  2.1- Model Kinds
Group, assembly, component all inherit from the base kind “model”
Subcomponent is the outlier

Only group models (group or assembly) can contain other models, and a prim can only be a model if its parent is also a group model (except the root).


<table>
  <tr>
    <th align="left">Structure</th>
  </tr>
  <tr>
  <td valign="top">
    
```usda
model
    component
    group
        assembly
subcomponent
```
</td> 
</table>

### 2.1.1- Group, assemblies
Group models serve as containers that can have other model children (unlike component models which are leaves), with assemblies being a specific type of group. Whereas the specialized group-model kind assembly generally identifies group models that are published assets, groups tend to be simple “inlined” model prims defined inside and as part of assemblies. They are the “glue” that holds a model hierarchy together.
 <table>
  <tr>
    <th align="left">Assembly example</th>
  </tr>
  <tr>
  <td valign="top">
    
```usda
def Xform "Forest_set" (
    kind = "assembly"
)
{
    def Xform "Outskirts" (
        kind = "group"
    )
    {
        # More deeply nested groups, bottoming out at references to other assemblies and components
    }

    def Xform "Glade" (
        kind = "group"
    )
    {
        # More deeply nested groups, bottoming out at references to other assemblies and components
    }
}
```
</td> 
</table>

Next exercises requires USDVIEW
##### 🧠 [Exercise (Groups)](https://docs.nvidia.com/learn-openusd/latest/asset-structure/model-hierarchy/exercise-groups.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/asset_structure)

##### 🧠 [Exercise (Assemblies)](https://docs.nvidia.com/learn-openusd/latest/asset-structure/model-hierarchy/exercise-assemblies.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/asset_structure)

### 2.1.2- Component
 A **component** is a reusable, self-contained asset that is complete and referenceable
 Complete assets like props, characters, or set pieces. They can contain subcomponents but cannot contain other models
 A component is a “leaf” kind of Model. Components can contain subcomponents, but no other models. Components can reference in other assets that are published as models, but they should override the kind of the referenced prim to “subcomponent”.

 <table>
  <tr>
    <th align="left">overriding the kind of a “nested” asset reference</th>
  </tr>
  <tr>
  <td valign="top">
    
```usda
def Xform "TreeSpruce" (
    kind = "component"
)
{
    # Geometry and shading prims that define a Spruce tree...

    def "Cone_1" (
        kind = "subcomponent"
        references = @Cones/PineConeA.usd@
    )
    {
    }
}
```
</td> 
</table>

##### 🧠 [Exercise (Components)](https://docs.nvidia.com/learn-openusd/latest/asset-structure/model-hierarchy/exercise-components.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/asset_structure)

##### 🧠 [Exercise (Variation Workstream)](https://docs.nvidia.com/learn-openusd/latest/asset-structure/model-hierarchy/exercise-variation-workstream.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/asset_structure)

🔗 [More info](https://docs.nvidia.com/learn-openusd/latest/beyond-basics/model-kinds.html)

##  2.2- Stage Traversal
 Stage traversal is the process of traversing the scenegraph of a stage with the purpose of querying or editing the scene data. We can traverse the scenegraph by iterating through child prims, accessing parent prims, and traversing the hierarchy to find specific prims of interest.

##### 🐍 i.e. (Traversing Through the Stage)
 <table>
  <td valign="top">
    
```usda
from pxr import Usd

stage: Usd.Stage = Usd.Stage.Open("_assets/stage_traversal.usda")

for prim in stage.Traverse():
    # Print the path of each prim
    print(prim.GetPath())
```
</td> 
</table>

##### 🐍 i.e. (Traversing USD Content for Specific Prim Types)
 <table>
  <td valign="top">
    
```usda
from pxr import Usd, UsdGeom

stage: Usd.Stage = Usd.Stage.Open("_assets/stage_traversal.usda")

scope_count = 0
xform_count = 0
for prim in stage.Traverse():
    if UsdGeom.Scope(prim):
        scope_count += 1
        print("Scope Type: ", prim.GetName())
    elif UsdGeom.Xform(prim):
        xform_count +=1
        print("Xform Type: ", prim.GetName())

print("Number of Scope prims: ", scope_count)
print("Number of Xform prims: ", xform_count)
```
</td> 
</table>

##### 🐍 i.e. (Traversing Using Usd.PrimRange)
 <table>
  <td valign="top">
    
```usda
from pxr import Usd
stage: Usd.Stage = Usd.Stage.Open("_assets/stage_traversal.usda")
prim_range = Usd.PrimRange(stage.GetPrimAtPath("/World/Box"))
for prim in prim_range:
    print(prim.GetPath())
```
</td> 
</table>

##### 🐍 i.e. (Traversal with Model Kinds)
 <table>
  <tr>
    <th align="left">Python code</th>
    <th align="left">USDA</th>
  </tr>
  <td valign="top">
    
```usda
from pxr import Usd, UsdGeom, Kind, Gf

# Create stage and model root
file_path = "_assets/model_kinds_component.usda"
stage = Usd.Stage.CreateNew(file_path)
world_xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world_xform.GetPrim())

# Make /World a group so children can be models
Usd.ModelAPI(world_xform.GetPrim()).SetKind(Kind.Tokens.group)

# Non-model branch: Markers (utility geometry, no kind)
markers = UsdGeom.Scope.Define(stage, world_xform.GetPath().AppendChild("Markers"))

points = {
    "PointA": Gf.Vec3d(-3, 0, -3), "PointB": Gf.Vec3d(-3, 0, 3),
    "PointC": Gf.Vec3d(3, 0, -3), "PointD": Gf.Vec3d(3, 0, 3)
    }
for name, pos in points.items():
    cone = UsdGeom.Cone.Define(stage, markers.GetPath().AppendChild(name))
    UsdGeom.XformCommonAPI(cone).SetTranslate(pos)
    cone.CreateDisplayColorPrimvar().Set([Gf.Vec3f(1.0, 0.85, 0.2)])

# Model branch: a Component we want to place as a unit
component = UsdGeom.Xform.Define(stage, world_xform.GetPath().AppendChild("Component"))
Usd.ModelAPI(component.GetPrim()).SetKind(Kind.Tokens.component)
body = UsdGeom.Cube.Define(stage, component.GetPath().AppendChild("Body"))
body.CreateDisplayColorPrimvar().Set([(0.25, 0.55, 0.85)])
UsdGeom.XformCommonAPI(body).SetScale((3.0, 1.0, 3.0))

# Model-only traversal: affect models, ignore markers
for prim in Usd.PrimRange(stage.GetPseudoRoot(), predicate=Usd.PrimIsModel):
    if prim.IsComponent():
        xformable = UsdGeom.Xformable(prim)
        if xformable:
            UsdGeom.XformCommonAPI(xformable).SetTranslate((0.0, 2.0, 0.0))

# Show which prims were considered models
model_paths = [p.GetPath().pathString for p in Usd.PrimRange(stage.GetPseudoRoot(), predicate=Usd.PrimIsModel)]
print("Model prims seen by traversal:", model_paths)

stage.Save()
```
</td> 
  <td valign="top">
    
```usda
#usda 1.0
(
    defaultPrim = "World"
)

def Xform "World" (
    kind = "group"
)
{
    def Scope "Markers"
    {
        def Cone "PointA"
        {
            color3f[] primvars:displayColor = [(1, 0.85, 0.2)]
            double3 xformOp:translate = (-3, 0, -3)
            uniform token[] xformOpOrder = ["xformOp:translate"]
        }

        def Cone "PointB"
        {
            color3f[] primvars:displayColor = [(1, 0.85, 0.2)]
            double3 xformOp:translate = (-3, 0, 3)
            uniform token[] xformOpOrder = ["xformOp:translate"]
        }

        def Cone "PointC"
        {
            color3f[] primvars:displayColor = [(1, 0.85, 0.2)]
            double3 xformOp:translate = (3, 0, -3)
            uniform token[] xformOpOrder = ["xformOp:translate"]
        }

        def Cone "PointD"
        {
            color3f[] primvars:displayColor = [(1, 0.85, 0.2)]
            double3 xformOp:translate = (3, 0, 3)
            uniform token[] xformOpOrder = ["xformOp:translate"]
        }
    }

    def Xform "Component" (
        kind = "component"
    )
    {
        double3 xformOp:translate = (0, 2, 0)
        uniform token[] xformOpOrder = ["xformOp:translate"]

        def Cube "Body"
        {
            color3f[] primvars:displayColor = [(0.25, 0.55, 0.85)]
            float3 xformOp:scale = (3, 1, 3)
            uniform token[] xformOpOrder = ["xformOp:scale"]
        }
    }
}
```
</td> 
</table>

##  2.3- Asset Structure 

The Four Principles of Scalable Asset Structure
- **Legibility** ensures your asset structure is easy to understand and interpret.
- **Modularity** allows for flexibility and reusability.
- **Performance** ensures your asset structure is efficient and optimized.
- **Navigability** makes it easy for users to find and access the features and properties they need.

### 2.3.1- Collections

##### ⭐ Example "Collections"

The following example shows a single prim with two collections. The relCollection collection is a relationship-mode collection that includes all objects at the /World/Clothing/Shirts and /World/Clothing/Pants paths. The expCollection collection is a pattern-based collection that matches all objects at the /World/Clothing/Shirts path that start with “Red”, and any descendants of those objects.

 <table>
  <td valign="top">
    
```usda
def "CollectionPrim" (
    prepend apiSchemas = ["CollectionAPI:relCollection", "CollectionAPI:expCollection"]
)
{
    # Specify collection membership using "includes"
    rel collection:relCollection:includes = [
        </World/Clothing/Shirts>,
        </World/Clothing/Pants>,
    ]

    # Specify collection membership using a path expression
    pathExpression collection:expCollection:membershipExpression = "/World/Clothing/Shirts/Red*//"
}
```
  </td>
</table>

If you want go deeper in collections, in the next link you will find detailed info with examples.

🔗 [More info](https://openusd.org/release/user_guides/collections_and_patterns.html#collections-and-patterns)

### 2.3.1- Asset Interface

Each asset designed to be opened as a stage or added to a scene through referencing has a root layer that serves as its foundation.

##### 🧠 [Exercise (Your First Asset)](https://docs.nvidia.com/learn-openusd/latest/asset-structure/asset-structure-principles/your-first-asset.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/asset_structure/exercise_01)

##### 🧠 [Exercise (Encapsulating Your Asset)](https://docs.nvidia.com/learn-openusd/latest/asset-structure/asset-structure-principles/encapsulating-your-asset.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/asset_structure/exercise_02)

##### 🧠 [Exercise (Organizing Prim Hierarchy)](https://docs.nvidia.com/learn-openusd/latest/asset-structure/asset-structure-principles/organizing-prim-hierarchy.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/asset_structure/exercise_03)

### 2.3.2- WorkStreams

Assets should model workstreams into layers.

##### 🧠 [Exercise (Adding User Workstreams)](https://docs.nvidia.com/learn-openusd/latest/asset-structure/workstreams/adding-user-workstreams.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/asset_structure/exercise_04)

### 2.3.3- Asset Parameterization
Asset parameterization enables the reuse of content by allowing certain fields and properties to vary downstream.

##### 🧠 [Exercise (Reuse content)](https://docs.nvidia.com/learn-openusd/latest/asset-structure/asset-parameterization/exercise-asset-parameterization.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/asset_structure/exercise_05)

### 2.3.4- Reference/Payload Pattern

Instead of expecting users to know whether a complex asset requires payloading, many assets adopt the “reference-payload” pattern. This means their interface file is designed to be referenced, with the payload structure internal to the asset.

##### 🧠 [Exercise (Reference/Payload Pattern)](https://docs.nvidia.com/learn-openusd/latest/asset-structure/reference-payload-pattern/exercise-ref-payload-pattern.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/asset_structure/exercise_06)

We use Lofting to show properties from payloaded assets to the layer from which we are referencing

##### 🧠 [Exercise (Lofting Primvars)](https://docs.nvidia.com/learn-openusd/latest/asset-structure/reference-payload-pattern/lofting-primvars.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/asset_structure/exercise_07)

##### 🧠 [Exercise (Lofting Variant Sets)](https://docs.nvidia.com/learn-openusd/latest/asset-structure/reference-payload-pattern/lofting-variant-sets.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/asset_structure/exercise_08)

### 2.3.5- Model Hierarchy



# 3) Customizing USD: Exam Weight 6%
# 4) Data Exchange: Exam Weight 15%
# 5) Data Modeling: Exam Weight 13%
# 6) Debugging and Troubleshooting: Exam Weight 11%
# 7) Pipeline Development: Exam Weight 14%
# 8) Visualization: Exam Weight 8%















