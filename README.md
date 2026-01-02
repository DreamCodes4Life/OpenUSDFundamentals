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

•   A **[primvar](https://openusd.org/release/glossary.html#usdglossary-primvar)** (primitive variable) is a special kind of attribute that can vary and interpolate across a geometric primitive. You work with primvars through UsdGeomImageable and UsdGeomPrimvar. Review its **[class](https://openusd.org/release/api/class_usd_geom_primvar.html)**. See **[Primvar Data Management](https://docs.omniverse.nvidia.com/usd/code-docs/usd-exchange-sdk/latest/api/group__primvars.html)**

•	Composition is cached, value resolution is not

•	Composition is internally multi-threaded, value resolution is meant to be client multi-threaded. USD’s primary guidance for clients wishing to maximize USD’s performance on multi-core systems is to perform as much simultaneous value resolution and data extraction as possible

•	Composition rules vary by composition arc, value resolution rules vary by metadatum.

•	An **index**, also referred to as a PrimIndex, is the result of composition. A prim’s index contains an ordered (from strongest to weakest) list of “Nodes”. All of the queries on USD classes except for stage-level metadata rely on prim indices to perform value resolution.


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
    
```py
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

```py
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
  
```py
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
  
```py
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
  
```py
#usda 1.0
(
    subLayers = [
        @./someAnimation.usd@ (offset = 10; scale = 0.5)
    ]
)
```
  </td> 
  <td>
    
```py
This USD will resolve as next:
A timesample of 30 in the someAnimation will be
resolved here at: 30*0.5 + 10 = 25.
Layer offsets cannot vary themselves over time
```
  </td> 
</table>

#### <ins>LayerStack:</ins> 
The ordered set of layers resulting from the recursive gathering of all SubLayers of a Layer, plus the layer itself as first and strongest.


##### 🧠 [Exercise (SubLayers)](https://docs.nvidia.com/learn-openusd/latest/creating-composition-arcs/sublayers/working-with-sublayers.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/sublayers)

##### 🧠 [Tutorial (Transformations, Animation, and Layer Offsets)](https://openusd.org/release/tut_xforms.html) 


What happens to “overs” when their underlying prim is moved to a different location in the scenegraph?

##### ⭐ Example "Sequence.usd"
---
<table>
  <tr>
    <th align="left">Sequence.usd/th>
    <th align="left">notes</th>
  </tr>
  <tr>
    <td valign="top">
  
```py
#usda 1.0

def Xform "World"
{
    def Xform "Sets"
    {
        def Xform "Bookshelf"
        {
            def Xform "Book_1"
            {
                string name = "Toy Story"
            }
        }

        def Xform "Desk"
        {
        }
    }
}

```
  </td> 
  <td valign="top">
    
```py

In this example, the book defined in sequence.usda has the title “Toy Story”. However, this layer is brought in to shot.usda via a sublayer statement, and the book’s title is overridden to “Wall-E.” The question is: what happens if a user independently working on sequence.usda moves Book_1 to Desk, or if Book_1 is renamed to Video_1? In such a case, the “over” in shot.usda would be “orphaned” and be ignored when composing and evaluating /World/Sets/Desk/Book_1 in shot.usda. It is the responsibility of the user working on sequence.usda to ensure that shot.usda is updated to avoid this problem.
```
</td> 
</table>


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
  
```py
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
    
```py
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
    
```py
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
  
```py
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
    
```py
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
  
```py
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
  
```py
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
    
```py
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
    
```py
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
  
```py
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
    
```py
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
  
```py
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
    
```py
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
    
```py
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
    
```py
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
    
```py
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
    
```py
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
    
```py
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
    
```py
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
    
```py
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
    
```py
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
    
```py
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
    
```py
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

```py
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
    
```py
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
    
```py
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

##  2.1- Model Kinds, Model Hierarchy

Model kinds are prim‑level metadata that classify a prim’s role in the model hierarchy.

The model hierarchy defines a contiguous set of prims descending from a root prim on a stage, all of which are models. Model hierarchy is an index of the scene that is, strictly, a prefix, of the entire scene.

Group, assembly, component all inherit from the base kind “model”
Subcomponent is the outlier

Only group models (group or assembly) can contain other models, and a prim can only be a model if its parent is also a group model (except the root).


<table>
  <tr>
    <th align="left">Structure</th>
  </tr>
  <tr>
  <td valign="top">
    
```py
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
    
```py
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
    
```py
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
    
```py
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
    
```py
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
    
```py
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
    
```py
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
    
```py
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

##### 🧠 [Exercise/Tutorial (Traversing a Stage)](https://openusd.org/release/tut_traversing_stage.html)

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
    
```py
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

### 2.3.2- Asset Interface

Each asset designed to be opened as a stage or added to a scene through referencing has a root layer that serves as its foundation.

##### 🧠 [Exercise (Your First Asset)](https://docs.nvidia.com/learn-openusd/latest/asset-structure/asset-structure-principles/your-first-asset.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/asset_structure/exercise_01)

##### 🧠 [Exercise (Encapsulating Your Asset)](https://docs.nvidia.com/learn-openusd/latest/asset-structure/asset-structure-principles/encapsulating-your-asset.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/asset_structure/exercise_02)

##### 🧠 [Exercise (Organizing Prim Hierarchy)](https://docs.nvidia.com/learn-openusd/latest/asset-structure/asset-structure-principles/organizing-prim-hierarchy.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/asset_structure/exercise_03)

### 2.3.3- WorkStreams

Assets should model workstreams into layers.

##### 🧠 [Exercise (Adding User Workstreams)](https://docs.nvidia.com/learn-openusd/latest/asset-structure/workstreams/adding-user-workstreams.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/asset_structure/exercise_04)

### 2.3.4- Asset Parameterization
Asset parameterization enables the reuse of content by allowing certain fields and properties to vary downstream.

##### 🧠 [Exercise (Reuse content)](https://docs.nvidia.com/learn-openusd/latest/asset-structure/asset-parameterization/exercise-asset-parameterization.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/asset_structure/exercise_05)

### 2.3.5- Reference/Payload Pattern

Instead of expecting users to know whether a complex asset requires payloading, many assets adopt the “reference-payload” pattern. This means their interface file is designed to be referenced, with the payload structure internal to the asset.

##### 🧠 [Exercise (Reference/Payload Pattern)](https://docs.nvidia.com/learn-openusd/latest/asset-structure/reference-payload-pattern/exercise-ref-payload-pattern.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/asset_structure/exercise_06)

We use Lofting to show properties from payloaded assets to the layer from which we are referencing

##### 🧠 [Exercise (Lofting Primvars)](https://docs.nvidia.com/learn-openusd/latest/asset-structure/reference-payload-pattern/lofting-primvars.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/asset_structure/exercise_07)

##### 🧠 [Exercise (Lofting Variant Sets)](https://docs.nvidia.com/learn-openusd/latest/asset-structure/reference-payload-pattern/lofting-variant-sets.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/asset_structure/exercise_08)

## 2.4- Asset Modularity and Instancing

### 2.4.1- Instancing

Instancing in USD is a feature that allows many instances of “the same” object to share the same representation (composed prims) on a UsdStage. Instances can be overridden in stronger layers, so it is possible to “break” an instance when necessary, if it must be uniquified.

Instancing in USD is a feature that allows many instances of “the same” object to share the same representation (composed prims) on a UsdStage. In exchange for this sharing of representation (which provides speed and memory benefits both for the USD core and, generally, for clients processing the UsdStage), we give up the ability to uniquely override opinions on prims beneath the “instance root”, although it is possible to override opinions that will affect all instances’ views of the data. 

In the next example, we create a class _Class_Cube_Red, then three cubes are instances of that class, the first two have modified position, the second has change opinion to a blue material, but is weaker so still will be red, the third is the same but this time is stronger, so the third cube will be blue without modifying the instance status.

##### ⭐ Example "Instancing a red cube and change opinion in instances"

<table>
    <td valign="top">
  
```py
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
  
```py
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

### 2.4.2- Authoring Scenegraph Instancing

Scenegraph–or native–instancing is the first implementation of instancing in OpenUSD.

There are four key terms involved in scenegraph instancing that you need to be aware of:

- Prototype: A unique, shared sub-structure

- Instance: A repetition of a prototype within a scene

- Instanceable Prim or Instance Prim: The mutable root of an instance

- Instance Proxy: A read-only addressable stand-in of the prototype prims of an instance

To enable scenegraph instancing in USD, you need to set one value, the instanceable prim metadata. Setting instanceable = true tells OpenUSD to create one shared version (prototype) of an object that many instances can use as long as they share composition arcs.

Proxies and instance subgraphs are immutable, but the instanceable prim is mutable.

##### 🧠 [Exercise (Author Scenegraph Instancing)](https://docs.nvidia.com/learn-openusd/latest/asset-modularity-instancing/authoring-scenegraph-instancing/exercise-authoring-scenegraph-instancing.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/Instancing/ex_sg_author_inst)

<u>Nested Instancing</u>
___

Nested instancing is when an instance subgraph has instances within it. 

##### 🧠 [Exercise (Nested Scenegraph Instancing)](https://docs.nvidia.com/learn-openusd/latest/asset-modularity-instancing/authoring-scenegraph-instancing/exercise-nested-instancing.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/Instancing/ex_sg_nested_inst)

### 2.4.3- Refining Scenegraph Instances

##### 🧠 [Exercise (Instance Editability)](https://docs.nvidia.com/learn-openusd/latest/asset-modularity-instancing/refining-scenegraph-instances/scenegraph-instance-refinement.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/Instancing/ex_sg_editability)

##### 🧠 [Exercise (Deinstance Refinement)](https://docs.nvidia.com/learn-openusd/latest/asset-modularity-instancing/refining-scenegraph-instances/scenegraph-deinstance-refinement.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/Instancing/ex_sg_deinstance_refine)

##### 🧠 [Exercise (Refinement Using Variant Sets)](https://docs.nvidia.com/learn-openusd/latest/asset-modularity-instancing/refining-scenegraph-instances/scenegraph-variant-set-refinement.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/Instancing/ex_sg_varset_refine)

Changes on inherited ancestral properties, like transforms, do not create any new prototypes; they simply leverage inheritance to efficiently introduce variety or control across instances.

You can also use primvars.

##### ⭐ Example "Refine Instances with primvars"

 <table>
  <td valign="top">
    
```py
#usda 1.0
(
    defaultPrim = "Warehouse"
    metersPerUnit = 0.01
    upAxis = "Z"
)
def Xform "Warehouse"
{
    def "RobotArm_01" (
        references = @./RobotArm.usd@
        instanceable = true
    )
    {
        color3f[] primvars:arm_color = [(0.61, 0.75, 0.24)] (
            interpolation = "constant"
        )
    }
    def "RobotArm_02" (
        references = @./RobotArm.usd@
        instanceable = true
    )
    {
    }
    def "RobotArm_03" (
        references = @./RobotArm.usd@
        instanceable = true
    )
    {
        color3f[] primvars:arm_color = [(0.08, 0.70, 0.52)] (
            interpolation = "constant"
        )
    }
    
}
```
  </td>
</table>

##### 🧠 [Exercise (Hierarchical Refinement Using Primvars)](https://docs.nvidia.com/learn-openusd/latest/asset-modularity-instancing/refining-scenegraph-instances/scenegraph-hierarchical-refinement.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/Instancing/ex_sg_primvar_refine)

##### 🧠 [Exercise (Ad Hoc Arcs Refinement)](https://docs.nvidia.com/learn-openusd/latest/asset-modularity-instancing/refining-scenegraph-instances/scenegraph-ad-hoc-arcs-refinement.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/Instancing/ex_sg_add_arc_refine)

##### 🧠 [Exercise (Broadcasted Refinement)](https://docs.nvidia.com/learn-openusd/latest/asset-modularity-instancing/refining-scenegraph-instances/scenegraph-broadcasted-refinement.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/Instancing/ex_sg_broadcasted_refine)

### 2.4.4- Authoring Point Instancing

Point instancing is implemented as a schema in OpenUSD–the PointInstancer prim type.

PointInstancer uses array attributes to describe points in 3D space. Additionally, explicit prototypes represented by prim hierarchies in the stage are specified as relationship targets on the PointInstancer. By combining the points, prototypes, and an index array to map the points to prototypes, OpenUSD is able to handle hundreds of thousands of repetitions very compactly in this vectorized format.

The PointInstancer includes the following mandatory properties:
- prototypes: A relationship targeting the prim hierarchies that the PointInstancer should use as instance prototypes.
- protoIndices Declares an instance of a prototype. Each element in the array maps a point to a prototype id.
- positions The points in local space where each instance is located.

##### 🧠 [Exercise (Authoring Point Instancing)](https://docs.nvidia.com/learn-openusd/latest/asset-modularity-instancing/authoring-point-instancing/exercise-authoring-point-instancing.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/Instancing/ex_pt_author)

### 2.4.5- Refining Point Instances

##### 🧠 [Exercise (Refining Point Instances)](https://docs.nvidia.com/learn-openusd/latest/asset-modularity-instancing/refining-point-instances.html) - [Material](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/Instancing/ex_pt_refine)

Note: Prototype prims do not exist in scene description – they are generated and managed internally by UsdStage. This allows UsdStage to create and remove prototypes as needed in response to scene description changes. For example, if some of the Car prims in ParkingLot.usd were changed to reference different assets, UsdStage would generate new prototype prims as needed. See Finding and Traversing Prototypes for information on how to use prototype prims.

🔗 [More info](https://openusd.org/release/api/class_usd_geom_point_instancer.html#details)
🔗 [More info 2](https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/Exercises/Instancing/ex_pt_refine)



# 3) Customizing USD: Exam Weight 6%

- **Model Kinds & Model Hierarchy** (Refer to 2.1)

## 3.1- Schema Classes

In the OpenUSD ecosystem, a schema is a blueprint that may define a new Prim type or Properties for describing a particular data model.  For example, a Geometry schema might specify how to define the vertices and topology of a 3D mesh, while a Shading schema could outline how to describe parameters for materials and textures.

Two types of Schemas:


| Aspect                    | ISA (Typed) Schemas                                           | API Schemas                                       |
| ------------------------- | ------------------------------------------------------------- | ------------------------------------------------- |
| **Purpose**               | Define *what a prim is*                                       | Define *what a prim can do*                       |
| **Schema Nature**         | **Concrete or Abstract**                                      | Always abstract                                   |
| **Prim Type Definition**  | Define or participate in prim type identity                   | Do not define a prim type                         |
| **Instantiation**         | Concrete schemas can be instantiated; abstract schemas cannot | Applied to existing prims                         |
| **Multiplicity per Prim** | ❌ Only one typed schema per prim                              | ✅ Multiple API schemas can be applied             |
| **Schema Role**           | Establish core structure, meaning, and inheritance            | Add reusable behavior or properties               |
| **Inheritance Model**     | Uses ISA (“is-a”) inheritance                                 | Uses composition via applied APIs                 |
| **Examples (Conceptual)** | Base geometry types, specialized prim categories              | Physics behavior, shading interfaces, constraints |

Note, all API schemas have API at the end of the name.

##### 🐍 Example: 

<table>
<tr>
<th align="left">Generic</th>
<th align="left">UsdGeom</th>
<th align="left">UsdLux</th>
<th align="left">UsdPhysics</th>
</tr>
<tr>
    
<td valign="top">

```py
# Retrieve the schema info for a registered schema
Usd.SchemaRegistry.FindSchemaInfo()

# Retrieve the schema typeName
Usd.SchemaRegistry.GetSchemaTypeName()


```
</td> 
<td valign="top">

```py
# Import related classes
from pxr import UsdGeom

# Define a sphere in the stage
sphere = UsdGeom.Sphere.Define(stage, "/World/Sphere")
	
# Get and Set the radius attribute of the sphere
sphere.GetRadiusAttr().Set(10)


```
</td> 

</td> 
<td valign="top">

```py
# Import related classes
from pxr import UsdLux

# Define a disk light in the stage
disk_light = UsdLux.DiskLight.Define(stage, "/World/Lights/DiskLight")
	
# Get all Attribute names that are a part of the DiskLight schema
dl_attribute_names = disk_light.GetSchemaAttributeNames()
	
# Get and Set the radius and intensity of the disk light prim
disk_light.GetRadiusAttr().Set(0.4)  # from DiskLight typed schema
disk_light.GetIntensityAttr().Set(1000)  # from LightAPI


```
</td> 
<td valign="top">

```py
# Import related classes
from pxr import UsdPhysics

# Apply a UsdPhysics Rigidbody API on the cube prim
cube_rb_api = UsdPhysics.RigidBodyAPI.Apply(cube.GetPrim())
	
# Get the Kinematic Enabled Attribute 
cube_rb_api.GetKinematicEnabledAttr()
	
# Create a linear velocity attribute of value 5
cube_rb_api.CreateVelocityAttr(5)

```
</td> 


</table>



##### ⭐ Example "schema for a sphere and ussage"

 <table>
  <tr>
    <th align="left">class Sphere</th>
    <th align="left">ussage</th>
  </tr>
  <td valign="top">
    
```py
class Sphere "Sphere" (
 
    inherits = </Gprim>
 
) {
 
    double radius = 1.0
 
    float3[] extent = [(-1.0, -1.0, -1.0), (1.0, 1.0, 1.0)] 
 
}
```
  </td>
  <td valign="top">
    
```py
def Sphere "MySphere" {
 
}
```
  </td>
</table>

A schema class is simply a container of a UsdPrim that provides a layer of specific, named API atop the underlying scene graph. 

Two types:

| Aspect                               | IsA schema                                                                 | API schema                                                                                         |
|--------------------------------------|----------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------|
| Main role                            | Defines *what a prim is* (its typed schema / prim type).                  | Adds *behaviors or properties* to an existing prim type.                                          |
| typeName                             | **Can author a `typeName`** for the prim, so the prim “is a” that type. :contentReference[oaicite:0]{index=0} | **Cannot author a `typeName`**; never defines the prim’s type. :contentReference[oaicite:1]{index=1} |
| Concrete vs abstract                 | Can be **concrete** (instantiable typed prim) or **non-concrete** (abstract base). :contentReference[oaicite:2]{index=2} | Considered **non-concrete** with respect to prim typing (they don’t create a new prim type). :contentReference[oaicite:3]{index=3} |
| Base class                           | Must derive (directly or indirectly) from **`UsdTyped`**. :contentReference[oaicite:4]{index=4}              | Derives from **`UsdAPISchemaBase`** (or `APISchemaBase` in the schema file). :contentReference[oaicite:5]{index=5} |
| How many per prim                    | A prim can have **at most one** IsA schema (one `typeName`). :contentReference[oaicite:6]{index=6}          | A prim can have **many** API schemas applied at once. :contentReference[oaicite:7]{index=7}          |
| How it’s attached to a prim          | By setting the prim’s `typeName` to the IsA schema’s type.                | By applying it via API (e.g. `Apply()`), recorded in prim metadata (`apiSchemas`) for applied APIs. :contentReference[oaicite:8]{index=8} |
| Fallback properties & schema registry| Definitions go into the schema registry and can provide fallback values. :contentReference[oaicite:9]{index=9} | Applied API schemas also go into the registry and can add built-ins with fallbacks. :contentReference[oaicite:10]{index=10} |
| Inheritance                          | Can form inheritance hierarchies (abstract → concrete typed schemas). :contentReference[oaicite:11]{index=11} | Cannot inherit from other API schemas (only from `UsdAPISchemaBase` / compatible API type). :contentReference[oaicite:12]{index=12} |
| Typical usage                        | “This prim **is a** light, mesh, scope, etc.”                             | “This prim **has** collections, clips, material bindings, render props, etc.”                     |
| Example from core USD                | `UsdGeomScope`, `UsdGeomMesh`, `UsdGeomImageable` (non-concrete). :contentReference[oaicite:13]{index=13} | `UsdModelAPI`, `UsdClipsAPI`, `UsdCollectionAPI`, `UsdGeomModelAPI`, `UsdGeomMotionAPI`. :contentReference[oaicite:14]{index=14} |

### 3.1.1- Generating New Schema Classes

Basic Guide To Creating Custom Schemas:

---

Creating new Prim types can range from simple definitions to complex structures like a Mesh. Here’s a brief on generating new schema classes:

Configure the Environment: Ensure Python modules like “jinja2” and “argparse” are installed.
Define the Schema Class: A schema class is a container of a UsdPrim. It provides a specific API atop the underlying scene graph.
Types of Schema Classes:
IsA schema: Imparts a typeName to a Prim, can be concrete or abstract.
API schema: Provides an interface but doesn’t specify a typeName.

Configure Environment: [Watch the tutorial on YouTube](https://youtu.be/ulZMQLSNgyQ)

USD provides a code generator script called ‘usdGenSchema’ for creating new schema classesThe schema generation script ‘usdGenSchema’ is driven by a USD layer.
- Must specify the libraryName as layer metadata.
- usd/schema.usda must exist in the layer stack, not necessarily as a direct subLayer.
- Schema typenames must be unique across all libraries.
- Attribute names and tokens must be camelCased valid identifiers.

base layer (or starting point) for creating new schema classes

##### ⭐ Example "base layer (or starting point) for creating new schema classes "

 <table>
  <td valign="top">
    
```py
#usda 1.0
(
    """ This file describes an example schema for code generation using
        usdGenSchema.
    """
    subLayers = [
        # To refer to schema types defined in schema.usda files from other
        # libraries, simply add comma-separated lines of the form
        # @<library name>/schema.usda@. In this example, we're referring
        # to schema types from 'usd'. If you were adding sub-classes of
        # UsdGeom schema types, you would use usdGeom/schema.usda instead.
        @usd/schema.usda@
    ]
)

over "GLOBAL" (
    customData = {
        string libraryName       = "usdSchemaExamples"
        string libraryPath       = "./"
        string libraryPrefix     = "UsdSchemaExamples"
    }
) {
}
```
  </td>
</table>

##### ⭐ Example Typed, Non-Concrete, IsA Schema

 <table>
  <tr>SimplePrim.usda</tr>
  <td valign="top">
    
```py
#usda 1.0
class "SimplePrim" (
    doc = """An example of an untyped schema prim. Note that it does not
             specify a typeName"""
    # IsA schemas should derive from </Typed>, which is defined in the
    # sublayer usd/schema.usda.
    inherits = </Typed>
    customData = {
        # Provide a different class name for the C++ and python schema
        # classes. This will be prefixed with libraryPrefix.
        # In this case, the class name becomes UsdSchemaExamplesSimple.
        string className = "Simple"
    }
)  {
    int intAttr = 0 (
        doc = "An integer attribute with fallback value of 0."
    )
    rel target (
        doc = """A relationship called target that could point to another
                 prim or a property"""
    )
}
```
  </td>
</table>

##### ⭐ Example Concrete IsA Schema

 <table>
  <tr>SimplePrim.usda</tr>
  <td valign="top">
    
```py
#usda 1.0
class ComplexPrim "ComplexPrim" (
    doc = """An example of a untyped IsA schema prim"""
    # Inherits from </SimplePrim> defined in simple.usda.
    inherits = </SimplePrim>
    customData = {
        string className = "Complex"
    }
)  {
    string complexString = "somethingComplex"
}

```
  </td>
</table>


##### ⭐ Example Applied API Schema

 <table>
  <tr>SimplePrim.usda</tr>
  <td valign="top">
    
```py
#usda 1.0
# API schemas only provide an interface to the prim's qualities.
# They are not allowed to specify a typeName.
class "ParamsAPI" (
    # IsA schemas should derive from </APISchemaBase>, which is defined in
    # the sublayer usd/schema.usda.
    inherits = </APISchemaBase>
    customData = {
        token apiSchemaType = "singleApply"
    }
)
{
    double params:mass (
        # Informs schema generator to create GetMassAttr() instead of
        # GetParamsMassAttr() method
        customData = {
            string apiName = "mass"
        }
        doc = "Double value denoting mass"
    )
    double params:velocity (
        customData = {
            string apiName = "velocity"
        }
        doc = "Double value denoting velocity"
    )
    double params:volume (
        customData = {
            string apiName = "volume"
        }
        doc = "Double value denoting volume"
    )
}
```
  </td>
</table>

You can find the previous examples in the USD_ROOT in the next path:
.\usd_root\share\usd\examples\plugin\usdSchemaExamples\resources\usdSchemaExamples\schema.usda

##### 🧠 Exercise [Generate and use the previouse schema samples](https://openusd.org/release/tut_generating_new_schema.html)

| Step | Description | Command / Output |
|------|-------------|------------------|
| 1 | Initialize the schema module (creates build helper files) | `.\scripts\usdInitSchema.bat share\usd\examples\plugin\usdSchemaExamples\resources\usdSchemaExamples .` |
| 2 | Re-run codegen so everything is in sync (optional but clean) | `.\scripts\usdGenSchema.bat share\usd\examples\plugin\usdSchemaExamples\resources\usdSchemaExamples\schema.usda share\usd\examples\plugin\usdSchemaExamples\resources\usdSchemaExamples` |
| 3 | Files created by `usdInitSchema` (if missing) | - `CMakeLists.txt`<br>- `__init__.py`<br>- `module.cpp`<br>- `schemaUserDoc.usda` |

🔗 [Full Guide](https://openusd.org/release/api/_usd__page__generating_schemas.html)


## 3.2- Extending the KindRegistry

The kind registry can be extended using the facilities provided by PlugRegistry, by adding a 'Kinds' sub-dictionary to the plugInfo.json file of any module within your "pixar-base aware" build environment. The dictionary entries will look like the following:

##### ⭐ Example Applied API Schema

 <table>
  <tr>SimplePrim.usda</tr>
  <td valign="top">
    
```py
"Info": {
    "Kinds": {
        "chargroup": {
            "baseKind": "assembly",
            "description": "A chargroup is an assembly comprised of a single character plus some associated models -- typically hair, garments, and charprops."
        },
        "charprop": {
            "baseKind": "component"
        },
        "newRootKind": {
        }
    }
}
```
  </td>
</table>

🔗 [Full Guide](https://openusd.org/release/api/kind_page_front.html)

## 3.3- Registering Plug-ins

🔗 [More Info](https://openusd.org/release/api/class_plug_registry.html#plug_RegisteringPlugins)

## 3.4- Asset Resolution

🔗 [More Info](https://openusd.org/release/api/ar_page_front.html)

# 4) Data Exchange: Exam Weight 15%

In USD, Data Exchange refers to the ability to share, modify, and synchronize scene data across different tools, applications, and teams using a layered, non-destructive composition model, where data from a source application is mapped and translated into a format that the destination application can understand. This mapping ensures that structure, meaning, and intent are preserved across systems, enabling geometry, materials, transforms, variants, and metadata to be exchanged consistently without destructive overwrites or loss of context.

There are four common implementations for adding OpenUSD support for your data format or application:
- Importers
- Exporters
- Standalone converters: a script, executable or microservice dedicated to translating to and from another file format.
- File format plugins. They allow OpenUSD to compose with additional file formats and even non-file-based sources, such as databases and procedurally generated content. They can be used as standalone converters with tools like usdcat.

Two-phase approach: extract and transform. This is loosely inspired by Extract-Transform-Load (ETL)

## 4.1- Install OpenUSD Exchange SDK

 <table>
   <tr>
    <th align="left">Windows</th>
    <th align="left">Linux</th>
  </tr>
  <td valign="top">

    # Create a virtual environment
    python -m venv usdex-env

    # Activate the virtual environment
    usdex-env\Scripts\activate

    # Install the OpenUSD Exchange modules
    pip install usd-exchange
  </td>
    <td valign="top">

    # Create a virtual environment
    python -m venv usdex-env

    # Activate the virtual environment
    source usdex-env/bin/activate

    # Install the OpenUSD Exchange modules
    pip install usd-exchange
  </td>
</table>

from omni.usd import get_context
stage = get_context().get_stage()

🔗 [Full Guide](https://docs.omniverse.nvidia.com/usd/code-docs/usd-exchange-sdk/latest/docs/getting-started.html)

##### 🐍 Example: Hello usdex

<table>
<tr>
<th align="left">From App</th>
<th align="left">From Python env</th>
</tr>
<tr>
    
<td valign="top">
    
```py
# hello_usdex.py
import pathlib
import usdex.core
from pxr import Gf, Usd, UsdGeom
from omni.usd import get_context

stage = get_context().get_stage()
root_layer = stage.GetRootLayer()
identifier = root_layer.identifier

UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(stage, 0.01)

# Create and Xform and set the transform on it
xform = usdex.core.defineXform(stage, "/Scene")
cube = UsdGeom.Cube.Define(stage, xform.GetPrim().GetPath().AppendChild("Cube"))
usdex.core.setLocalTransform(
    prim=cube.GetPrim(),
    translation=Gf.Vec3d(10.459, 49.592, 17.792),
    pivot=Gf.Vec3d(0.0),
    rotation=Gf.Vec3f(-0.379, 56.203, 0.565),
    rotationOrder=usdex.core.RotationOrder.eXyz,
    scale=Gf.Vec3f(1),
)

# Save the stage
stage.Save()

print(f"Created USD stage '{pathlib.Path('./'+identifier).absolute()}' using:")
print(f"\tOpenUSD version: {Usd.GetVersion()}")
print(f"\tOpenUSD Exchange SDK version: {usdex.core.version()}")
```
</td> 
<td valign="top">

```py
# hello_usdex.py
import pathlib
import usdex.core
from pxr import Gf, Usd, UsdGeom

# Create a new USD stage
identifier = "hello_world.usda"
stage = usdex.core.createStage(identifier, "Scene", UsdGeom.Tokens.y, 0.01, "OpenUSD Exchange SDK Example")

# Create and Xform and set the transform on it
xform = usdex.core.defineXform(stage, "/Scene")
cube = UsdGeom.Cube.Define(stage, xform.GetPrim().GetPath().AppendChild("Cube"))
usdex.core.setLocalTransform(
    prim=cube.GetPrim(),
    translation=Gf.Vec3d(10.459, 49.592, 17.792),
    pivot=Gf.Vec3d(0.0),
    rotation=Gf.Vec3f(-0.379, 56.203, 0.565),
    rotationOrder=usdex.core.RotationOrder.eXyz,
    scale=Gf.Vec3f(1),
)

# Save the stage
stage.Save()

print(f"Created USD stage '{pathlib.Path('./'+identifier).absolute()}' using:")
print(f"\tOpenUSD version: {Usd.GetVersion()}")
print(f"\tOpenUSD Exchange SDK version: {usdex.core.version()}")
```
</td>
</table>

When authoring UsdStages it is important to configure certain metrics & metadata on the root SdfLayer of the stage.
Available Functions: configureStage, createStage, saveStage. Detailed in the next link.

🔗 [Review Functions](https://docs.omniverse.nvidia.com/usd/code-docs/usd-exchange-sdk/latest/api/group__stage__metadata.html)

When authoring UsdPrims to a Stage, you will need to specify an SdfPath that identifies a unique location for the Prim. The nature of OpenUSD’s composition algorithm (know as “LIVERPS”) makes it fairly complex to determine whether your chosen location is valid for authoring. 

🔗 [Review Functions](https://docs.omniverse.nvidia.com/usd/code-docs/usd-exchange-sdk/latest/api/group__stage__hierarchy.html)

Introspection of USD layers

🔗 [Review Functions](https://docs.omniverse.nvidia.com/usd/code-docs/usd-exchange-sdk/latest/api/group__layers.html)

##### 🧠 [Exercise (Anatomy of a Converter)](https://docs.nvidia.com/learn-openusd/latest/data-exchange/data-exchange/exercise.html)


## 4.2- Data Extraction

To achieve a direct and faithful extraction between two data formats, [conceptual](https://docs.omniverse.nvidia.com/usd/latest/technical_reference/conceptual_data_mapping/index.html) data mapping is crucial. This process involves analyzing how to map data models from one format to another.

🔗 [More Info](https://docs.nvidia.com/learn-openusd/latest/data-exchange/data-extraction/what-is-data-extraction.html)

##### 🧠 [Exercise (Extracting Geometry)](https://docs.nvidia.com/learn-openusd/latest/data-exchange/data-exchange/exercise.html)

##### 🧠 [Exercise (Extracting Materials)](https://docs.nvidia.com/learn-openusd/latest/data-exchange/data-extraction/exercise-extracting-materials.html)

##### 🐍 Example: Full Data Exchange from OBJ

<table>
<tr>
<th align="left">Final result from previous exercises</th>
</tr>
<tr>
    
<td valign="top">
    
```py

import argparse
import logging
import math
from enum import Enum
from pathlib import Path

import assimp_py
from pxr import Gf, Sdf, Tf, Usd, UsdGeom, UsdShade

logger = logging.getLogger("obj2usd")


class UpAxis(Enum):
    Y = UsdGeom.Tokens.y
    Z = UsdGeom.Tokens.z

    def __str__(self):
        return self.value

# ADD CODE BELOW HERE
# vvvvvvvvvvvvvvvvvvv

def extract(input_file: Path, output_file: Path) -> Usd.Stage:
    logger.info("Executing extraction phase...")
    process_flags = 0
    # Load the obj using Assimp 
    scene = assimp_py.ImportFile(str(input_file), process_flags)
    # Define the stage where the output will go 
    stage: Usd.Stage = Usd.Stage.CreateNew(str(output_file))

    for mesh in scene.meshes:
        # Replace any invalid characters with underscores.
        sanitized_mesh_name = Tf.MakeValidIdentifier(mesh.name)
        usd_mesh = UsdGeom.Mesh.Define(stage, f"/{sanitized_mesh_name}")
        # You can use the Vt APIs here instead of Python lists.
        # Especially keep this in mind for C++ implementations.
        face_vertex_counts = []
        face_vertex_indices = []
        for indices in mesh.indices:
            # Convert the indices to a flat list
            face_vertex_indices.extend(indices)
            # Append the number of vertices for each face
            face_vertex_counts.append(len(indices))
        
        usd_mesh.CreatePointsAttr(mesh.vertices)
        usd_mesh.CreateFaceVertexCountsAttr().Set(face_vertex_counts)
        usd_mesh.CreateFaceVertexIndicesAttr().Set(face_vertex_indices)
        # Treat the mesh as a polygonal mesh and not a subdivision surface.
        # Respect the normals or lack of normals from OBJ.
        usd_mesh.CreateSubdivisionSchemeAttr(UsdGeom.Tokens.none)
        if mesh.normals:
            usd_mesh.CreateNormalsAttr(mesh.normals)
        
        # Get the mesh's material by index
        # scene.materials is a dictionary consisting of assimp material properties
        mtl = scene.materials[mesh.material_index]
        if not mtl:
            continue
        sanitized_mat_name = Tf.MakeValidIdentifier(mtl["NAME"])
        material_path = Sdf.Path(f"/{sanitized_mat_name}")
        # Create the material prim
        material: UsdShade.Material = UsdShade.Material.Define(stage, material_path)
        # Create a UsdPreviewSurface Shader prim.
        shader: UsdShade.Shader = UsdShade.Shader.Define(stage, material_path.AppendChild("Shader"))
        shader.CreateIdAttr("UsdPreviewSurface")
        # Connect shader surface output as an output for the material graph.
        material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), UsdShade.Tokens.surface)
        # Get colors
        diffuse_color = mtl["COLOR_DIFFUSE"]
        emissive_color = mtl["COLOR_EMISSIVE"]
        specular_color = mtl["COLOR_SPECULAR"]
        # Convert specular shininess to roughness.
        roughness = 1 - math.sqrt(mtl["SHININESS"] / 1000.0)

        shader.CreateInput("useSpecularWorkflow", Sdf.ValueTypeNames.Int).Set(1)
        shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(diffuse_color))
        shader.CreateInput("emissiveColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(emissive_color))
        shader.CreateInput("specularColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(specular_color))
        shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(roughness)
        binding_api = UsdShade.MaterialBindingAPI.Apply(usd_mesh.GetPrim())
        binding_api.Bind(material)

    return stage


def transform(stage: Usd.Stage, args: argparse.Namespace):
    logger.info("Executing transformation phase...")


def main(args: argparse.Namespace):
    # Extract the .obj
    stage: Usd.Stage = extract(args.input, args.output)
    # Transformations to be applied to the scene hierarchy
    transform(stage, args)
    # Save the Stage after editing
    stage.Save()

# ^^^^^^^^^^^^^^^^^^^^
# ADD CODE ABOVE HERE


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(
        "obj2usd", description="An OBJ to USD converter script."
    )
    parser.add_argument("input", help="Input OBJ file", type=Path)
    parser.add_argument("-o", "--output", help="Specify an output USD file", type=Path)
    export_opts = parser.add_argument_group("Export Options")
    export_opts.add_argument(
        "-u",
        "--up-axis",
        help="Specify the up axis for the exported USD stage.",
        type=UpAxis,
        choices=list(UpAxis),
        default=UpAxis.Y,
    )

    args = parser.parse_args()
    if args.output is None:
        args.output = args.input.parent / f"{args.input.stem}.usda"

    logger.info(f"Converting {args.input}...")
    main(args)
    logger.info(f"Converted results output as: {args.output}.")
    logger.info(f"Done.")

```
</td> 

</table>

## 4.3- Asset Validation

Omniverse Asset Validator is based on usdchecker and provides a GUI for asset validation. The asset validator includes:
- User interface
- Command line interface
- Python API
- Automatic fixes for failed validations
- Ability to add new rules

##### 🧠 [Exercise (Asset Validation and Testing)](https://docs.nvidia.com/learn-openusd/latest/data-exchange/asset-validation/exercise-asset-validation-testing.html)

## 4.4- Data Transformation

Key aspects of data transformation include:
- Export options
- Content re-structuring
- Optimizations, e.g., mesh merging

A transformation step doesn’t need to happen in the same process as extraction or other transformation steps. It could be a separate process or a cloud service. You can even consider transformations that may occur as post-processes after a stage has been exported or converted.

##### 🧠 [Exercise (Transforming the Prim Hierarchy)](https://docs.nvidia.com/learn-openusd/latest/data-exchange/data-transformation/transformation-hierarchy.html)

##### 🧠 [Exercise/Tutorial (Converting Between Layer Formats)](https://openusd.org/release/tut_converting_between_layer_formats.html)

## 4.5- Converting Between Layer Formats

File formats:

| Order | Arc Type |
|-----|---------|
| **.usda** | Human-readable UTF-8 text |
| **.usdc** | Random-access “Crate” binary |
| **.usd** | Either of the above |

usdcat can be used to convert files between file formats. With plain, .usd files, you can change them using the --usdFormat option.

$ usdcat file.usd --out file.usd --usdFormat usda

🔗 [More Info](https://openusd.org/release/usdfaq.html#so-what-file-formats-does-usd-support)

🔗 [More Info](https://openusd.org/release/toolset.html#usdcat)

**Converting between .usda and .usdc Files**

A .usd file can be either a text or binary format file. When USD opens a .usd file, it detects the underlying format and handles the file appropriately. You can convert any .usda or .usdc file to a .usd file simply by renaming it. 

Consider Sphere.usda
To convert this file to binary, we can specify an output filename with the .usdc extension:
$ usdcat -o NewSphere.usdc Sphere.usda
This produces a binary file named Sphere.usdc in the current directory containing the same content as Sphere.usda. We can verify this using usddiff:
$ usddiff Sphere.usda NewSphere.usdc

Same goes for the other way around

🔗 [Full details](https://openusd.org/release/tut_converting_between_layer_formats.html)

Usdz File Format Specification

A single object, from marshaling and transmission perspectives
Potentially streamable
Usable without unpacking to a filesystem

A usdz package is an uncompressed zip archive that is allowed to contain the following file types:

| Kind | Allowed File Types |
|-----|---------|
| USD | usda, usdc, usd |
| Image | png, jpeg, exr, avif |
| Audio | M4A, MP3, WAV |

- A usdz package is a zero compression, unencrypted zip archive.
- it is possible to reference individual files within a package from outside the package
- packages can themselves contain other packages
- A usdz file is read-only - editing its contents requires first unpacking the package and editing its constituent parts using appropriate tools. Since usdz is a “core” USD file format, one can use usdcat and usdedit on packages:

🔗 [Full details](https://openusd.org/release/spec_usdz.html)

## 4.6- Maximizing USD Performance

### 4.6.1- Use an allocator optimized for multithreading

### 4.6.2- Use binary “.usd” files for geometry and shading caches

For files that contain more than a few small definitions or overrides, the binary “usdc” format will open faster and consume substantially much less memory while held open (a UsdStage keeps open all the layers that participate in a composition). You should not need to exert any extra effort to get this behavior since creating a new layer or stage with a filename someFile.usd will, by default, create a usdc file.

### 4.6.3- Package assets with payloads

# 5) Data Modeling: Exam Weight 13%

##  5.0- Before you start, things you need to know

•	A **prim path** describes where a prim lives in the scene hierarchy. Prims are objects such as geometry, lights, transforms, etc. 

•	Extending a prim path with a . and a property name gives you a **property path**. Properties include attributes (data values) and relationships (connections between prims). 

•	USD paths can include **variant selections**, using curly braces to specify which variant of a prim is being referenced. 


## 5.1- Setting the Stage

### 5.1.1- Stage

At its core, an OpenUSD stage presents the scenegraph, which dictates what is in our scene.


##### 🐍 Example: Create a USD File and Load it as a Stage

<table>
<tr>
<th align="left">first_stage.usda</th>
</tr>
<tr>
    
<td valign="top">
    
```py

# Import the `Usd` module from the `pxr` package:
from pxr import Usd

# Define a file path name:
file_path = "_assets/first_stage.usda"
# Create a stage at the given `file_path`:
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)
print(stage.ExportToString(addSourceFileComment=False))
```
</td> 

</table>


##### 🐍 Example: Create a USD File and Load it as a Stage

<table>
<tr>
<th align="left">first_stage.usda</th>
</tr>
<tr>
    
<td valign="top">
    
```py

# Import the `Usd` module from the `pxr` package:
from pxr import Usd

# Define a file path name:
file_path = "_assets/first_stage.usda"
# Create a stage at the given `file_path`:
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)
print(stage.ExportToString(addSourceFileComment=False))
```
</td> 

</table>

##### 🐍 Example: Open and Save USD Stages

<table>
<tr>
<th align="left">first_stage.usda</th>
</tr>
<tr>
    
<td valign="top">
    
```py

from pxr import Usd

# Open an existing USD stage from disk:
stage: Usd.Stage = Usd.Stage.Open("_assets/first_stage.usda")

# Add a simple prim so we can see a change in the saved file:
stage.DefinePrim("/World", "Xform")

# Save the stage back to disk:
stage.Save()

# Print the stage as text so we can inspect the result:
print(stage.ExportToString(addSourceFileComment=False))
```
</td> 

</table>


##### 🐍 Example: Create a Stage in Memory

Sometimes you may want to create a stage without immediately writing it to disk. This is useful when generating temporary data, running tests, or building a stage that you only want to save after validating its contents.

<table>
<tr>
<th align="left">in_memory_stage.usda</th>
</tr>
<tr>
    
<td valign="top">
    
```py

from pxr import Usd

# Create a new stage stored only in memory:
stage: Usd.Stage = Usd.Stage.CreateInMemory()

# Add a prim so the stage contains some data:
stage.DefinePrim("/World", "Xform")

# Print the stage's contents:
print("In-memory stage:")
print(stage.ExportToString(addSourceFileComment=False))

# Export the stage to disk if needed:
stage.Export("_assets/in_memory_stage.usda")
```
</td> 

</table>

##### 🐍 Example: Working With the Root Layer

When you create a stage with CreateNew(), the file you pass becomes its root layer.

<table>
<tr>
<th align="left">root_layer_example.usda</th>
</tr>
<tr>
    
<td valign="top">
    
```py

from pxr import Usd, Sdf
import os

# Create a new stage:
stage: Usd.Stage = Usd.Stage.CreateNew("_assets/root_layer_example.usda")

# Get the root layer object:
root_layer: Sdf.Layer = stage.GetRootLayer()
# Use relpath to avoid printing build machine filesystem info.
print("Root layer identifier:", os.path.relpath(root_layer.identifier))

# Add a simple prim so the stage is not empty:
stage.DefinePrim("/World", "Xform")

# Create an additional layer (in a different format) and add it as a sublayer:
extra_layer: Sdf.Layer = Sdf.Layer.CreateNew("_assets/extra_layer.usdc")
# Anchor the path relative to the root layer for better portability
rel_path = "./" + os.path.basename(extra_layer.identifier)
root_layer.subLayerPaths.append(rel_path)

# Save both layers:
stage.Save()
extra_layer.Save()

# Print the contents of the root layer:
print("Root layer contents:")
print(root_layer.ExportToString())
```
</td> 

</table>

🔗 [Full details](https://docs.nvidia.com/learn-openusd/latest/stage-setting/stage.html)

### 5.1.2- Prims

If you followed the previous subjects you have already worked a lot with prims. A prim is the primary container object in USD. It can contain other prims and properties holding data.

##### 🐍 Example: Defining a Prim

DefinePrim() API provides a generic way to create any type of prim:

<table>
<tr>
<th align="left">Python snippet</th>
<th align="left">prims.usda</th>
</tr>
<tr>
    
<td valign="top">
    
```py
# Import the `Usd` module from the `pxr` package:
from pxr import Usd

# Create a new USD stage with root layer named "prims.usda":
stage: Usd.Stage = Usd.Stage.CreateNew("_assets/prims.usda")

# Define a new primitive at the path "/hello" on the current stage:
stage.DefinePrim("/hello")

# Define a new primitive at the path "/world" on the current stage with the prim type, Sphere.
stage.DefinePrim("/world", "Sphere")

stage.Save()
```
</td> 
<td valign="top">
    
```py
#usda 1.0

def "hello"
{
}

def Sphere "world"
{
}
```
</td> 

</table>

##### 🐍 Example: Defining a Sphere Prim

Using a specific API to create a prim

<table>
<tr>
<th align="left">Python snippet</th>
<th align="left">sphere_prim.usda</th>
</tr>
<tr>
    
<td valign="top">

```py
from pxr import Usd, UsdGeom

file_path = "_assets/sphere_prim.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

# Define a prim of type `Sphere` at path `/hello`:
sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, "/hello")
sphere.CreateRadiusAttr().Set(2)

# Save the stage:
stage.Save()


```
</td> 
<td valign="top">

```py
#usda 1.0

def Sphere "hello"
{
    double radius = 2
}


```
</td> 

</table>

##### 🐍 Example: Creating a Prim Hierarchy

<table>
<tr>
<th align="left">python</th>
<th align="left"></th>
</tr>
<tr>
    
<td valign="top">

```py
from pxr import Usd, UsdGeom

file_path = "_assets/prim_hierarchy.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

# Define a Scope prim in stage at `/Geometry`
geom_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, "/Geometry")
# Define an Xform prim in the stage as a child of /Geometry called GroupTransform
xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, geom_scope.GetPath().AppendPath("GroupTransform"))
# Define a Cube in the stage as a child of /Geometry/GroupTransform, called Box
cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, xform.GetPath().AppendPath("Box"))

stage.Save()


```
</td> 
<td valign="top">

```py
#usda 1.0

def Scope "Geometry"
{
    def Xform "GroupTransform"
    {
        def Cube "Box"
        {
        }
    }
}


```
</td> 

</table>


##### 🐍 Example: Does the Prim Exist?

<table>
<tr>
<th align="left">python</th>
<th align="left">prim_hierarchy.usda</th>
</tr>
<tr>
    
<td valign="top">

```py
from pxr import Usd

file_path = "_assets/prim_hierarchy.usda"
stage: Usd.Stage = Usd.Stage.Open(file_path)

prim: Usd.Prim = stage.GetPrimAtPath("/Geometry")
child_prim: Usd.Prim
if child_prim := prim.GetChild("Box"):
    print("Child prim exists")
else:
    print("Child prim DOES NOT exist")


```
</td> 
<td valign="top">

```py
#usda 1.0

def Scope "Geometry"
{
    def Xform "GroupTransform"
    {
        def Cube "Box"
        {
        }
    }
}


```
</td> 

</table>


### 5.1.3- Properties

Prims can have two types of properties: attributes and relationships. Attributes are the most common type of property authored in most USD scenes. An attribute can take on exactly one of the legal attribute typeNames USD provides, and can take on both a default value and an animated value. Resolving an attribute at any given timeCode will yield either a single value or no value. Attributes resolve according to “strongest wins” rules, so all values for any given attribute will be fetched from the strongest PrimSpec that provides either a default value or an animated value. Note that this simple rule is somewhat more complicated in the presence of authored value clips. One interacts with attributes through the UsdAttribute API.

 - **Attributes**

 Each attribute can have a default value, and it can also have different values at different points in time, called time samples.

##### 🐍 Example: Retrieving Properties of a Prim

<table>
<tr>
<th align="left">Code</th>
<th align="left">attributes_ex1.usda</th>
</tr>
<tr>
    
<td valign="top">

```py
from pxr import Usd, UsdGeom, Gf

file_path = "_assets/attributes_ex1.usda"

stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

# Define a sphere under the World xForm:
sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world_xform.GetPath().AppendPath("Sphere"))

# Define a cube under the World xForm and set it to be 5 units away from the sphere:
cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendPath("Cube"))
UsdGeom.XformCommonAPI(cube).SetTranslate(Gf.Vec3d(5, 0, 0))

# Get the property names of the cube prim:
cube_prop_names = cube.GetPrim().GetPropertyNames()

# Print the property names:
for prop_name in cube_prop_names:
    print(prop_name)

stage.Save()


```
</td> 
<td valign="top">

```py
#usda 1.0

def Xform "World"
{
    def Sphere "Sphere"
    {
    }

    def Cube "Cube"
    {
        double3 xformOp:translate = (5, 0, 0)
        uniform token[] xformOpOrder = ["xformOp:translate"]
    }
}


```
</td> 

</table>
 
##### 🐍 Example: Getting Attribute Values

<table>
<tr>
<th align="left">Code</th>
<th align="left">attributes_ex2.usda</th>
</tr>
<tr>
    
<td valign="top">

```py
from pxr import Usd, UsdGeom, Gf

file_path = "_assets/attributes_ex2.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world_xform.GetPath().AppendPath("Sphere"))
cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendPath("Cube"))
UsdGeom.XformCommonAPI(cube).SetTranslate(Gf.Vec3d(5, 0, 0))

# Get the attributes of the cube prim
cube_attrs = cube.GetPrim().GetAttributes()
for attr in cube_attrs:
    print(attr)

# Get the size, display color, and extent attributes of the cube
cube_size: Usd.Attribute = cube.GetSizeAttr()
cube_displaycolor: Usd.Attribute = cube.GetDisplayColorAttr()
cube_extent: Usd.Attribute = cube.GetExtentAttr()

print(f"Size: {cube_size.Get()}")
print(f"Display Color: {cube_displaycolor.Get()}")
print(f"Extent: {cube_extent.Get()}")

stage.Save()


```
</td> 
<td valign="top">

```py
def Xform "World"
{
    def Sphere "Sphere"
    {
    }

    def Cube "Cube"
    {
        double3 xformOp:translate = (5, 0, 0)
        uniform token[] xformOpOrder = ["xformOp:translate"]
    }
}


```
</td> 

</table>

##### 🐍 Example: Setting Attribute Values

<table>
<tr>
<th align="left">Code</th>
<th align="left">attributes_ex3.usda</th>
</tr>
<tr>
    
<td valign="top">

```py
from pxr import Usd, UsdGeom, Gf

file_path = "_assets/attributes_ex3.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world_xform.GetPath().AppendPath("Sphere"))
cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendPath("Cube"))
UsdGeom.XformCommonAPI(cube).SetTranslate(Gf.Vec3d(5,0,0))

# Get the size, display color, and extent attributes of the cube
cube_size: Usd.Attribute = cube.GetSizeAttr()
cube_displaycolor: Usd.Attribute = cube.GetDisplayColorAttr()
cube_extent: Usd.Attribute = cube.GetExtentAttr()

# Modify the size, extent, and display color attributes:
cube_size.Set(cube_size.Get() * 2)
cube_extent.Set(cube_extent.Get() * 2)
cube_displaycolor.Set([(0.0, 1.0, 0.0)])

stage.Save()


```
</td> 
<td valign="top">

```py
#usda 1.0

def Xform "World"
{
    def Sphere "Sphere"
    {
    }

    def Cube "Cube"
    {
        float3[] extent = [(-2, -2, -2), (2, 2, 2)]
        color3f[] primvars:displayColor = [(0, 1, 0)]
        double size = 4
        double3 xformOp:translate = (5, 0, 0)
        uniform token[] xformOpOrder = ["xformOp:translate"]
    }
}


```
</td> 

</table>

Similarly to how prims can be deactivated through composing overriding opinions, the value that an attribute produces can be blocked by an overriding opinion of None, which can be authored using UsdAttribute::Block().

In the next example, Usd.Attribute.Get(t) will return always none, because we cannot override in timeSamples, we could if we dont define 

##### ⭐ Example Attribute Block

<table>
<tr>
<th align="left">attributeBlock.usda</th>
</tr>
<tr>
    
<td valign="top">

```py
def Sphere "BigBall"
{
    double radius = 100
    double radius.timeSamples = {
        1: 100,
        24: 500,
    }
}

def "DefaultBall" (
    references = </BigBall>
)
{
    double radius = None
}


```
</td> 

</table>

🔗 [Full examples](https://openusd.org/release/glossary.html#usdglossary-attributeblock)

 🔗 [More Info](https://docs.nvidia.com/learn-openusd/latest/stage-setting/properties/attributes.html)

  - **Relationships**

Relationships establish connections between prims, acting as pointers or links between objects in the scene hierarchy. A relationship allows a prim to target or refer to other prims, attributes, or even other relationships. This establishes dependencies between scenegraph objects.

##### 🐍 Example: Prim Collections with Relationships

<table>
<tr>
<th align="left">Code</th>
<th align="left">relationships_ex1.usda</th>
</tr>
<tr>
    
<td valign="top">

```py
from pxr import Usd, UsdGeom, Gf

file_path = "_assets/relationships_ex1.usda"
stage = Usd.Stage.CreateNew(file_path)

world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

# Define a sphere under the World Xform:
sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world_xform.GetPath().AppendPath("Sphere"))

# Define a cube under the World Xform and set it to be 5 units away from the sphere:
cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendPath("Cube"))
UsdGeom.XformCommonAPI(cube).SetTranslate(Gf.Vec3d(5, 0, 0))

# Create typeless container for the group
group = stage.DefinePrim("/World/Group") 

# Define the relationship
group.CreateRelationship("members", custom=True).SetTargets(
    [sphere.GetPath(), cube.GetPath()]
)

# List relationship targets
members_rel = group.GetRelationship("members")
print("Group members:", [str(p) for p in members_rel.GetTargets()])

stage.Save()


```
</td> 
<td valign="top">

```py
#usda 1.0

def Xform "World"
{
    def Sphere "Sphere"
    {
    }

    def Cube "Cube"
    {
        double3 xformOp:translate = (5, 0, 0)
        uniform token[] xformOpOrder = ["xformOp:translate"]
    }

    def "Group"
    {
        custom rel members = [
            </World/Sphere>,
            </World/Cube>,
        ]
    }
}

```
</td> 

</table>

##### 🐍 Example: Using a Built‑in Relationship (proxyPrim)

<table>
<tr>
<th align="left">Code</th>
<th align="left">relationships_ex2.usda</th>
</tr>
<tr>
<td valign="top">

```py
from pxr import Usd, UsdGeom

file_path = "_assets/relationships_ex2.usda"
stage = Usd.Stage.CreateNew(file_path)

world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

# Define a "high cost" Sphere Prim under the World Xform:
high: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world_xform.GetPath().AppendPath("HiRes"))

# Define a "low cost" Cube Prim under World Xfrom
low: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendPath("Proxy"))

UsdGeom.Imageable(high).GetPurposeAttr().Set("render")
UsdGeom.Imageable(low).GetPurposeAttr().Set("proxy")

# Author the proxy link on the render Prim
UsdGeom.Imageable(high).GetProxyPrimRel().SetTargets([low.GetPath()])

# Tools that honor proxyPrim should draw the proxy in preview
draw_prim = UsdGeom.Imageable(high).ComputeProxyPrim()  # returns Usd.Prim
print("Preview should draw:", str(draw_prim[0].GetPath() if draw_prim else high.GetPath()))

stage.Save()

```
</td> 
<td valign="top">

```py
#usda 1.0

def Xform "World"
{
    def Sphere "HiRes"
    {
        rel proxyPrim = </World/Proxy>
        uniform token purpose = "render"
    }

    def Cube "Proxy"
    {
        uniform token purpose = "proxy"
    }
}

```
</td> 

</table>


##### 🐍 Example: Material Binding Relationships

<table>
<tr>
<th align="left">Code</th>
<th align="left">relationships_ex3.usda</th>
</tr>
<tr>
    
<td valign="top">

```py
from pxr import Usd, UsdGeom, UsdShade, Gf, Sdf

file_path = "_assets/relationships_ex3.usda"
stage = Usd.Stage.CreateNew(file_path)

world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")


cube_1: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendPath("Cube_1"))
cube_2: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendPath("Cube_2"))
UsdGeom.XformCommonAPI(cube_2).SetTranslate(Gf.Vec3d(5, 0, 0))
cube_3: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendPath("Cube_3"))
UsdGeom.XformCommonAPI(cube_3).SetTranslate(Gf.Vec3d(10, 0, 0))

# Create typeless container for the materials
looks = stage.DefinePrim("/World/Looks")

# Create simple green material for preview
green: UsdShade.Material = UsdShade.Material.Define(stage, looks.GetPath().AppendPath("GreenMat"))
green_ps = UsdShade.Shader.Define(stage, green.GetPath().AppendPath("PreviewSurface"))
green_ps.CreateIdAttr("UsdPreviewSurface")
green_ps.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(0.0, 1.0, 0.0))
green.CreateSurfaceOutput().ConnectToSource(green_ps.ConnectableAPI(), "surface")

# Create simple red material for preview
red: UsdShade.Material = UsdShade.Material.Define(stage, looks.GetPath().AppendPath("RedMat"))
red_ps = UsdShade.Shader.Define(stage, red.GetPath().AppendPath("PreviewSurface"))
red_ps.CreateIdAttr("UsdPreviewSurface")
red_ps.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(1.0, 0.0, 0.0))
red.CreateSurfaceOutput().ConnectToSource(red_ps.ConnectableAPI(), "surface")

# Bind materials to Prims
UsdShade.MaterialBindingAPI.Apply(cube_1.GetPrim()).Bind(green)
UsdShade.MaterialBindingAPI.Apply(cube_2.GetPrim()).Bind(green)
UsdShade.MaterialBindingAPI.Apply(cube_3.GetPrim()).Bind(red)

# Verify by reading the direct binding
for prim in [cube_1, cube_2, cube_3]:
    mat = UsdShade.MaterialBindingAPI(prim).GetDirectBinding().GetMaterial()
    print(f"{prim.GetPath()} -> {mat.GetPath() if mat else 'None'}")

stage.Save()

```
</td> 
<td valign="top">

```py
#usda 1.0

def Xform "World"
{
    def Cube "Cube_1" (
        prepend apiSchemas = ["MaterialBindingAPI"]
    )
    {
        rel material:binding = </World/Looks/GreenMat>
    }

    def Cube "Cube_2" (
        prepend apiSchemas = ["MaterialBindingAPI"]
    )
    {
        rel material:binding = </World/Looks/GreenMat>
        double3 xformOp:translate = (5, 0, 0)
        uniform token[] xformOpOrder = ["xformOp:translate"]
    }

    def Cube "Cube_3" (
        prepend apiSchemas = ["MaterialBindingAPI"]
    )
    {
        rel material:binding = </World/Looks/RedMat>
        double3 xformOp:translate = (10, 0, 0)
        uniform token[] xformOpOrder = ["xformOp:translate"]
    }

    def "Looks"
    {
        def Material "GreenMat"
        {
            token outputs:surface.connect = </World/Looks/GreenMat/PreviewSurface.outputs:surface>

            def Shader "PreviewSurface"
            {
                uniform token info:id = "UsdPreviewSurface"
                color3f inputs:diffuseColor = (0, 1, 0)
                token outputs:surface
            }
        }

        def Material "RedMat"
        {
            token outputs:surface.connect = </World/Looks/RedMat/PreviewSurface.outputs:surface>

            def Shader "PreviewSurface"
            {
                uniform token info:id = "UsdPreviewSurface"
                color3f inputs:diffuseColor = (1, 0, 0)
                token outputs:surface
            }
        }
    }
}

```
</td> 

</table>

  - **Connection**

Connections are quite similar to relationships in that they are list-edited “scene pointers” that robustly identify other scene objects. The key difference is that while relationships are typeless, independent properties, connections are instead a sub-aspect of USD attributes.

##### 🧠 [Tutorial (Simple Shading in USD)](https://openusd.org/release/tut_simple_shading.html)

### 5.1.4- Time Codes and Time Samples

We have already show a few examples of this, let's see one more example.

##### 🐍 Example: Bouncing ball sim

<table>
<tr>
<th align="left">Code 1 - Create timecode_sample.usda</th>
<th align="left">Code 2 - Create animation</th>
<th align="left">timecode_ex.usda</th>
</tr>
<tr>
    
<td valign="top">

```py
# Import the necessary modules from the `pxr` library:
from pxr import Usd, UsdGeom, Gf

# Create a new USD stage file named "timecode_ex.usda":
file_path = "_assets/timecode_sample.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

# Define a transform ("Xform") primitive at the "/World" path:
world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

# Define a Sphere primitive as a child of the transform at "/World/Sphere" path:
sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world.GetPath().AppendPath("Sphere"))

# Define a blue Cube as a background prim:
box: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world.GetPath().AppendPath("Backdrop"))
box.GetDisplayColorAttr().Set([(0.0, 0.0, 1.0)])
cube_xform_api = UsdGeom.XformCommonAPI(box)
cube_xform_api.SetScale(Gf.Vec3f(5, 5, 0.1))
cube_xform_api.SetTranslate(Gf.Vec3d(0, 0, -2))

# Save the stage to the file:
stage.Save()

```
</td> 
<td valign="top">

```py
from pxr import Usd, UsdGeom, Gf

# Open stage from example 2a
stage: Usd.Stage = Usd.Stage.Open("_assets/timecode_ex.usda")

sphere: UsdGeom.Sphere = UsdGeom.Sphere.Get(stage, "/World/Sphere")

if scale_attr := sphere.GetScaleOp().GetAttr():
    scale_attr.Clear()

sphere_xform_api = UsdGeom.XformCommonAPI(sphere)

# Set scale of the sphere at time 1
sphere_xform_api.SetScale(Gf.Vec3f(1.00, 1.00, 1.00), time=1)  
# Set scale of the sphere at time 30
sphere_xform_api.SetScale(Gf.Vec3f(1.00, 1.00, 1.00), time=30)   
# Set scale of the sphere at time 45
sphere_xform_api.SetScale(Gf.Vec3f(1.00, 0.20, 1.25), time=45)   
# Set scale of the sphere at time 50
sphere_xform_api.SetScale(Gf.Vec3f(0.75, 2.00, 0.75), time=50)  
# Set scale of the sphere at time 60
sphere_xform_api.SetScale(Gf.Vec3f(1.00, 1.00, 1.00), time=60)  

# Export to a new flattened layer for this example.
stage.Export("_assets/timecode_ex2b.usda", addSourceFileComment=False)

```
</td> 
</td> 
<td valign="top">

```py
#usda 1.0
(
    endTimeCode = 60
    startTimeCode = 1
)

def Xform "World"
{
    def Sphere "Sphere"
    {
        float3 xformOp:scale.timeSamples = {
            1: (1, 1, 1),
            30: (1, 1, 1),
            45: (1, 0.2, 1.25),
            50: (0.75, 2, 0.75),
            60: (1, 1, 1),
        }
        double3 xformOp:translate.timeSamples = {
            1: (0, 5.5, 0),
            30: (0, -4.5, 0),
            45: (0, -5, 0),
            50: (0, -3.25, 0),
            60: (0, 5.5, 0),
        }
        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:scale"]
    }

    def Cube "Backdrop"
    {
        color3f[] primvars:displayColor = [(0, 0, 1)]
        float3 xformOp:scale = (5, 5, 0.1)
        double3 xformOp:translate = (0, 0, -2)
        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:scale"]
    }
}

```
</td> 

</table>

##### ⭐ Example "TimeCodes Scaled to Real Time"
---
<table>
  <tr>
    <th align="left">example.usd</th>
    <th align="left">notes</th>
  </tr>
  <tr>
    <td>
  
```py
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
    
```py
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

### 5.1.5- Prim and Property Paths

In OpenUSD, a path is a string that uniquely identifies the location of a prim or property within a USD scenegraph hierarchy, similar to a filesystem path. The root of the scene is represented by /, and each nested prim is separated by /. For example:

/World/Geometry/Box

**Primary Uses of Paths**
Paths are fundamental in USD for:
- Uniquely identifying prims and their properties within a scene. 
- Navigating the scene hierarchy programmatically or via tools. 
- Authoring—specifying where to add or modify prims and properties on a stage. 
- Querying and filtering prims, such as with expressions that match certain path patterns. 

##### 🐍 Example: Getting, Validating, and Defining Prims at Path

<table>
<tr>
<th align="left">Code</th>
<th align="left">paths.usda</th>
</tr>
<tr>
    
<td valign="top">

```py
from pxr import Usd

stage: Usd.Stage = Usd.Stage.CreateNew("_assets/paths.usda")
stage.DefinePrim("/hello")
stage.DefinePrim("/hello/world")

# Get the primitive at the path "/hello" from the current stage
hello_prim: Usd.Prim = stage.GetPrimAtPath("/hello")

# Get the primitive at the path "/hello/world" from the current stage
hello_world_prim: Usd.Prim = stage.GetPrimAtPath("/hello/world")

# Get the primitive at the path "/world" from the current stage
# Note: This will return an invalid prim because "/world" does not exist, but if changed to "/hello/world" it will return a valid prim
world_prim: Usd.Prim = stage.GetPrimAtPath("/world")

# Print whether the primitive is valid
print("Is /hello a valid prim? ", hello_prim.IsValid())
print("Is /hello/world a valid prim? ", hello_world_prim.IsValid())
print("Is /world a valid prim? ", world_prim.IsValid())

stage.Save()


```
</td> 
<td valign="top">

```py
def "hello"
{
    def "world"
    {
    }
}


```
</td> 

</table>


##### 🐍 Example: Build and navigate prim paths with Sdf.Path

<table>
<tr>
<th align="left">Code</th>
<th align="left">paths_build_and_nav.usda</th>
</tr>
<tr>
    
<td valign="top">

```py
from pxr import Usd, UsdGeom, Sdf

stage = Usd.Stage.CreateNew("_assets/paths_build_and_nav.usda")

# Build prim paths via Sdf.Path
world_path = Sdf.Path("/World")
geometry_path = world_path.AppendChild("Geometry")  # /World/Geometry
sphere_path = geometry_path.AppendChild("Sphere")  # /World/Geometry/Sphere

looks_path = world_path.AppendChild("Looks")  # /World/Looks
material_path = looks_path.AppendChild("Material")  # /World/Looks/Material

# Define prims at those paths
stage.DefinePrim(world_path)
stage.DefinePrim(geometry_path)
UsdGeom.Sphere.Define(stage, sphere_path)
stage.DefinePrim(looks_path)
stage.DefinePrim(material_path)

# Path checks and basic navigation
print("sphere_path IsPrimPath:", sphere_path.IsPrimPath())
print("sphere_path parent:",    sphere_path.GetParentPath())
print("Geometry prim valid:",   stage.GetPrimAtPath(geometry_path).IsValid())
print("\nmaterial_path IsPrimPath:", material_path.IsPrimPath())
print("material_path parent:",    material_path.GetParentPath())
print("Looks prim valid:",   stage.GetPrimAtPath(looks_path).IsValid())

stage.Save()


```
</td> 
<td valign="top">

```py
#usda 1.0

def "World"
{
    def "Geometry"
    {
        def Sphere "Sphere"
        {
        }
    }

    def "Looks"
    {
        def "Material"
        {
        }
    }
}


```
</td> 

</table>


##### 🐍 Example: Author an attribute and a relationship from property paths

<table>
<tr>
<th align="left">Code</th>
<th align="left">paths_property_authoring.usda</th>
</tr>
<tr>
    
<td valign="top">

```py
from pxr import Usd, UsdGeom, Sdf

stage = Usd.Stage.CreateNew("_assets/paths_property_authoring.usda")

# A prim to work with
sphere = UsdGeom.Sphere.Define(stage, "/World/Geom/Sphere")

# Create a property path for the attribute /World/Geom/Sphere.userProperties:tag
attr_property_path = sphere.GetPath().AppendProperty("userProperties:tag")

# Working with the property path for the attribute
owner_prim = stage.GetPrimAtPath(attr_property_path.GetPrimPath())
attr_name = stage.GetPropertyAtPath(attr_property_path).GetPath().name  # "userProperties:tag"
print(f"Attribute property '{attr_name}' has been defined on {owner_prim.GetPath()} after AppendProperty: {owner_prim.GetAttribute(attr_name).IsDefined()}")

# Define the attribute on the owner prim
attr = owner_prim.CreateAttribute(attr_name, Sdf.ValueTypeNames.String)
print(f"\nAttribute property '{attr_name}' has been defined on {owner_prim.GetPath()} after CreateAttribute: {owner_prim.GetAttribute(attr_name).IsDefined()}")

attr.Set("surveyed")
print(f"Attribute value after Set: {stage.GetAttributeAtPath(attr_property_path).Get()}")

# Create a relationship from a property path
marker = UsdGeom.Xform.Define(stage, "/World/Markers/MarkerA")
# Create a property path for the relationship
rel_property_path = sphere.GetPath().AppendProperty("my:ref")  # /World/Geom/Sphere.my:ref

# Working with the property path for the relationship
owner_prim = stage.GetPrimAtPath(rel_property_path.GetPrimPath())
rel_name = stage.GetPropertyAtPath(rel_property_path).GetPath().name  # "my:ref"
print(f"\nRelationship property '{rel_name}' has been defined on {owner_prim.GetPath()} after AppendProperty: {owner_prim.GetRelationship(rel_name).IsDefined()}")

# Define the relationship on the owner prim
rel = owner_prim.CreateRelationship(rel_name)
print(f"\nRelationship property '{rel_name}' has been defined on {owner_prim.GetPath()} after CreateRelationship: {owner_prim.GetRelationship(rel_name).IsDefined()}")

rel.AddTarget(marker.GetPath())
print(f"Relationship targets after AddTarget: {[str(p) for p in stage.GetRelationshipAtPath(rel_property_path).GetTargets()]}")

stage.Save()


```
</td> 
<td valign="top">

```py
#usda 1.0

def "World"
{
    def "Geom"
    {
        def Sphere "Sphere"
        {
            custom rel my:ref
            prepend rel my:ref = </World/Markers/MarkerA>
            custom string userProperties:tag = "surveyed"
        }
    }

    def "Markers"
    {
        def Xform "MarkerA"
        {
        }
    }
}


```
</td> 

</table>





### 5.1.6- OpenUSD File Formats -> (go to 4.5)

### 5.1.7- OpenUSD Modules

OpenUSD modules are organized libraries within the USD codebase that expose specific functionality for building, querying, or extending USD scenes. They help structure USD’s capabilities into cohesive APIs for different purposes such as scene authoring, composition, geometry, math utilities, and more. 

Core USD Packages
<table width="100%"> <colgroup> <col style="width:20%"> <col style="width:25%"> <col style="width:55%"> </colgroup> <thead> <tr> <th>Name</th> <th>Type</th> <th>Description</th> </tr> </thead> <tbody> <tr> <td><b>base</b></td> <td>Core Package</td> <td>Foundational utilities and shared low-level functionality used across all USD modules</td> </tr> <tr> <td><b>usd</b></td> <td>Core Package</td> <td>Core APIs for authoring, composing, and reading USD scene data</td> </tr> <tr> <td><b>imaging</b></td> <td>Optional Package</td> <td>Rendering and visualization support for USD scenes</td> </tr> <tr> <td><b>usdImaging</b></td> <td>Optional Package</td> <td>USD-specific imaging adapters and renderer integration</td> </tr> </tbody> </table>

Commonly Used USD Modules
<table width="100%"> <colgroup> <col style="width:20%"> <col style="width:25%"> <col style="width:55%"> </colgroup> <thead> <tr> <th>Name</th> <th>Type</th> <th>Description</th> </tr> </thead> <tbody> <tr> <td><b>Usd</b></td> <td>Core Module</td> <td>High-level API for stages, prims, properties, metadata, and composition arcs</td> </tr> <tr> <td><b>Sdf</b></td> <td>Foundation Module</td> <td>Scene description foundation for layers, paths, serialization, and data structures</td> </tr> <tr> <td><b>Gf</b></td> <td>Utility Module</td> <td>Math and geometry types such as vectors, matrices, and quaternions</td> </tr> </tbody> </table>

Schema Modules
<table width="100%"> <colgroup> <col style="width:20%"> <col style="width:25%"> <col style="width:55%"> </colgroup> <thead> <tr> <th>Name</th> <th>Type</th> <th>Description</th> </tr> </thead> <tbody> <tr> <td><b>UsdGeom</b></td> <td>Schema Module</td> <td>Geometry primitives, transforms, and spatial data</td> </tr> <tr> <td><b>UsdShade</b></td> <td>Schema Module</td> <td>Materials, shaders, and shading networks</td> </tr> <tr> <td><b>UsdPhysics</b></td> <td>Schema Module</td> <td>Physical properties, simulation, and physics metadata</td> </tr> </tbody> </table>


### 5.1.8- Metadata

Metadata is “data about the data” in a USD scene: extra information that guides behavior, organization, and pipeline decisions but is not the primary scene content (like geometry values).

Metadata commonly stores things like:

- author / creation notes, annotations

- project- or pipeline-specific tags

- render / workflow hints or flags 

Metadata can be authored at different scopes (for example on a stage, prim, or property), enabling both global and localized control.

| Aspect                      | Metadata                                                     | Attributes                                                        |
| --------------------------- | ------------------------------------------------------------ | ----------------------------------------------------------------- |
| **Schema Relationship**     | Separate from the core schema data model                     | Defined explicitly by schemas                                     |
| **Intended Use**            | Supplementary and contextual information                     | Actual authored data that defines an object                       |
| **Role in Scene**           | Guides behavior, organization, or pipeline logic             | Describes concrete properties and state                           |
| **Time-Varying**            | ❌ Cannot be time-sampled                                     | ✅ Can be time-sampled                                             |
| **Performance Implication** | Often cheaper to store and evaluate                          | Time-sampling may increase evaluation cost                        |
| **Examples (Conceptual)**   | Tags, annotations, pipeline hints, ownership, workflow flags | Transform values, visibility, material parameters, animation data |


##### 🐍 Example: Working with metadata

<table>
<tr>
<th align="left">Code</th>
</tr>
<tr>
    
<td valign="top">

```py
# Retrieve the metadata value associated with the given key for a USD Object
usdobject.GetMetadata('key')

# Set the metadata value for the given key on a USD Object
usdobject.SetMetadata('key', value)

# Retrieve the metadata value associated with the given key for the stage
stage.GetMetadata('key')

# Set the metadata value for the given key on the stage
stage.SetMetadata('key', value) 

# Use for better performance if accessing a single value and not all the metadata within a key
GetMetadataByDictKey()


```
</td> 

</table>


## 5.2- Scene Description Blueprints

### 5.2.1- Schemas -> (go to 3.1)
### 5.2.2- Scope

The folders in USD. It does not represent any geometry or renderable content itself but acts as a container for organizing other prims

##### 🐍 Example: Define a Scope and check Active/Inactive

<table>
<tr>
<th align="left">Code</th>
<th align="left">scope.usda</th>
</tr>
<tr>
    
<td valign="top">

```py
from pxr import Usd, UsdGeom, Gf

file_path = "_assets/scope.usda"
stage = Usd.Stage.CreateNew(file_path)

# World container (transformable)
world = UsdGeom.Xform.Define(stage, "/World")

num_a_prims = 2
num_b_prims = 2

# Two organizational Scopes (non-transformable grouping prims)
a_scope = UsdGeom.Scope.Define(stage, world.GetPath().AppendPath("A_Scope"))
b_scope = UsdGeom.Scope.Define(stage, world.GetPath().AppendPath("B_Scope"))

# Populate the scopes with some geometry
for a in range(num_a_prims):
    sphere = UsdGeom.Sphere.Define(stage, a_scope.GetPath().AppendPath(f"A_Sphere_{a}"))
    UsdGeom.XformCommonAPI(sphere).SetTranslate(Gf.Vec3d(a*2.5, 0, 0))

for b in range(num_b_prims):
    cube = UsdGeom.Cube.Define(stage, b_scope.GetPath().AppendPath(f"B_Cube_{b}"))
    UsdGeom.XformCommonAPI(cube).SetTranslate(Gf.Vec3d(b*2.5, -2.5, 0))

# Deactivate the A_Scope
a_scope.GetPrim().SetActive(False)

stage.Save()


```
</td> 
<td valign="top">

```py



```
</td> 

</table>




### 5.2.3- Xform

In OpenUSD, an Xform is a type of prim that stores transformation data, such as translation, rotation, and scaling, which apply to its child prims.

##### 🐍 Example: UsdGeom and Xform

<table>
<tr>
<th align="left">Code</th>
<th align="left">xform_prim.usda</th>
</tr>
<tr>
    
<td valign="top">

```py
# Import the necessary modules from the pxr package:
from pxr import Usd, UsdGeom

# Create a new USD stage with root layer named "xform_prim.usda":
file_path = "_assets/xform_prim.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

# Define a new Xform primitive at the path "/World" on the current stage:
world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

# Save changes to the current stage to its root layer:
stage.Save()
print(stage.ExportToString(addSourceFileComment=False))


```
</td> 
<td valign="top">

```py
#usda 1.0

def Xform "World"
{
}


```
</td> 

</table>


### 5.2.4- XformCommonAPI
This API facilitates the authoring and retrieval of a common set of operations with a single translation, rotation, scale and pivot that is generally compatible with import and export into many tools. It’s designed to simplify the interchange of these transformations.

##### 🐍 Example: XformCommonAPI - Transforms and Inheritance

<table>
<tr>
<th align="left">Code</th>
<th align="left">xformcommonapi.usda</th>
</tr>
<tr>
    
<td valign="top">

```py
from pxr import Usd, UsdGeom, Gf

file_path = "_assets/xformcommonapi.usda"
stage = Usd.Stage.CreateNew(file_path)

# A root transform group we will move and rotate
world = UsdGeom.Xform.Define(stage, "/World")
parent = UsdGeom.Xform.Define(stage, world.GetPath().AppendPath("Parent_Prim"))

# Parent Translate, Rotate, Scale using XformCommonAPI
parent_xform_api = UsdGeom.XformCommonAPI(parent)
parent_xform_api.SetTranslate(Gf.Vec3d(5, 0, 3))
parent_xform_api.SetRotate(Gf.Vec3f(90, 0, 0))
parent_xform_api.SetScale(Gf.Vec3f(3.0, 3.0, 3.0))


child_translation = Gf.Vec3d(2, 0, 0)

# Child A - inherits parent transforms
child_a_cone = UsdGeom.Cone.Define(stage, parent.GetPath().AppendChild("Child_A"))
child_a_xform_api = UsdGeom.XformCommonAPI(child_a_cone)
child_a_xform_api.SetTranslate(child_translation)  # Parent_Prim transform + local placement

# Child B - "/World/Alt_Parent/Child_B" does NOT inherit Parent_Prim transforms
alt_parent = UsdGeom.Xform.Define(stage, world.GetPath().AppendChild("Alt_Parent"))
child_b_cone = UsdGeom.Cone.Define(stage, alt_parent.GetPath().AppendChild("Child_B"))
child_b_xform_api = UsdGeom.XformCommonAPI(child_b_cone)
child_b_xform_api.SetTranslate(child_translation)  # local placement only

# Inspect the authored Xform Operation Order
print("Parent xformOpOrder:", UsdGeom.Xformable(parent).GetXformOpOrderAttr().Get())
print("Alt_Parent xformOpOrder:", UsdGeom.Xformable(alt_parent).GetXformOpOrderAttr().Get())
print("Child A xformOpOrder:", UsdGeom.Xformable(child_a_cone).GetXformOpOrderAttr().Get())
print("Child B xformOpOrder:", UsdGeom.Xformable(child_b_cone).GetXformOpOrderAttr().Get())

stage.Save()


```
</td> 
<td valign="top">

```py
#usda 1.0

def Xform "World"
{
    def Xform "Parent_Prim"
    {
        float3 xformOp:rotateXYZ = (90, 0, 0)
        float3 xformOp:scale = (3, 3, 3)
        double3 xformOp:translate = (5, 0, 3)
        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:rotateXYZ", "xformOp:scale"]

        def Cone "Child_A"
        {
            double3 xformOp:translate = (2, 0, 0)
            uniform token[] xformOpOrder = ["xformOp:translate"]
        }
    }

    def Xform "Alt_Parent"
    {
        def Cone "Child_B"
        {
            double3 xformOp:translate = (2, 0, 0)
            uniform token[] xformOpOrder = ["xformOp:translate"]
        }
    }
}


```
</td> 

</table>

### 5.2.5- Lights

UsdLux is the schema domain that includes a set of light types and light-related schemas. It provides a standardized way to represent various types of lights, such as:

- Directional lights (UsdLuxDistantLight)
- Area lights, including
- Cylinder lights (UsdLuxCylinderLight)
- Rectangular area lights (UsdLuxRectLight)
- Disk lights (UsdLuxDiskLight)
- Sphere lights (UsdLuxSphereLight)
- Dome lights (UsdLuxDomeLight)
- Portal lights (UsdLuxPortalLight)

##### 🐍 Example: UsdLux and DistantLight

<table>
<tr>
<th align="left">Code</th>
<th align="left">distant_light.usda</th>
</tr>
<tr>
    
<td valign="top">

```py
from pxr import Usd, UsdGeom, UsdLux

file_path = "_assets/distant_light.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
geo_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, world.GetPath().AppendPath("Geometry"))
box_geo: UsdGeom.Cube = UsdGeom.Cube.Define(stage, geo_scope.GetPath().AppendPath("Cube"))

# Define a new Scope primitive at the path "/World/Lights" on the current stage:
lights_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, world.GetPath().AppendPath("Lights"))

# Define a new DistantLight primitive at the path "/World/Lights/SunLight" on the current stage:
distant_light: UsdLux.DistantLight = UsdLux.DistantLight.Define(stage, lights_scope.GetPath().AppendPath("SunLight"))

stage.Save()


```
</td> 
<td valign="top">

```py
#usda 1.0

def Xform "World"
{
    def Scope "Geometry"
    {
        def Cube "Cube"
        {
        }
    }

    def Scope "Lights"
    {
        def DistantLight "SunLight"
        {
        }
    }
}


```
</td> 

</table>

##### 🐍 Example: Setting Light Properties

<table>
<tr>
<th align="left">Code</th>
<th align="left">light_props.usda</th>
</tr>
<tr>
    
<td valign="top">

```py
from pxr import Gf, Usd, UsdGeom, UsdLux

file_path = "_assets/light_props.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)
geom_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, "/Geometry")
cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, geom_scope.GetPath().AppendPath("Box"))

# Define a `Scope` Prim in stage at `/Lights`:
lights_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, "/Lights")

# Define a `Sun` prim in stage as a child of `lights_scope`, called `Sun`:
distant_light = UsdLux.DistantLight.Define(stage, lights_scope.GetPath().AppendPath("Sun"))
# Define a `SphereLight` prim in stage as a child of lights_scope called `SphereLight`:
sphere_light = UsdLux.SphereLight.Define(stage, lights_scope.GetPath().AppendPath("SphereLight"))

# Configure the distant light's emissive attributes:
distant_light.GetColorAttr().Set(Gf.Vec3f(1.0, 0.0, 0.0)) # Light color (red)
distant_light.GetIntensityAttr().Set(120.0) # Light intensity
# Lights are Xformable
if not (distant_light_xform_api := UsdGeom.XformCommonAPI(distant_light)):
    raise Exception("Prim not compatible with XformCommonAPI")
distant_light_xform_api.SetRotate((45.0, 0.0, 0.0))


# Configure the sphere light's emissive attributes:
sphere_light.GetColorAttr().Set(Gf.Vec3f(0.0, 0.0, 1.0)) # Light color (blue)
sphere_light.GetIntensityAttr().Set(50000.0) # Light intensity
# Lights are Xformable
if not (sphere_light_xform_api := UsdGeom.XformCommonAPI(sphere_light)):
    raise Exception("Prim not compatible with XformCommonAPI")
sphere_light_xform_api.SetTranslate((5.0, 10.0, 0.0))

stage.Save()


```
</td> 
<td valign="top">

```py
#usda 1.0

def Scope "Geometry"
{
    def Cube "Box"
    {
    }
}

def Scope "Lights"
{
    def DistantLight "Sun"
    {
        color3f inputs:color = (1, 0, 0)
        float inputs:intensity = 120
        float3 xformOp:rotateXYZ = (45, 0, 0)
        uniform token[] xformOpOrder = ["xformOp:rotateXYZ"]
    }

    def SphereLight "SphereLight"
    {
        color3f inputs:color = (0, 0, 1)
        float inputs:intensity = 50000
        double3 xformOp:translate = (5, 10, 0)
        uniform token[] xformOpOrder = ["xformOp:translate"]
    }
}


```
</td> 

</table>


## 5.3- Beyond the Basics



### 5.3.1- Primvars

We have already been working with Primvars all along, and had a small description in 1.0. Let's dig deeper.

Primvars support several interpolation modes, based on interpolation modes of the primvar equivalent Primitive Variable from RenderMan. These are:

- **constant**: One value remains constant over the entire surface prim. Note that only constant interpolation primvars will inherit down the namespace.
- **uniform**: One value remains constant for each UV patch segment of the surface prim (which is a face for meshes).
- **varying**: Four values are interpolated over each UV patch segment of the surface. Bilinear interpolation is used for interpolation between the four values.
- **vertex**: Values are interpolated between each vertex in the surface prim. The basis function of the surface is used for interpolation between vertices.
- **faceVarying**: For polygons and subdivision surfaces, four values are interpolated over each face of the mesh. Bilinear interpolation is used for interpolation between the four values.

##### ⭐ Example Using Constant Interpolation

<table>
<tr>
<th align="left">constant.usda</th>
<th align="left">Result</th>
</tr>
<tr>
    
<td valign="top">

```py
#usda 1.0
(
)

def Mesh "constant"
{
   float3[] extent = [(-1, 0, 0), (1, 1, 0)]
   point3f[] points = [(-1, 0, 0), (-1, 1, 0), (0, 1, 0), (0, 0, 0), (1, 1, 0), (1, 0, 0)]
   int[] faceVertexCounts = [4, 4]
   int[] faceVertexIndices = [3, 2, 1, 0, 5, 4, 2, 3]

   color3f[] primvars:displayColor = [(1, 0, 0)] (
       interpolation = "constant"
   )

   double3 xformOp:translate = (0, 0, -10)
   uniform token[] xformOpOrder = ["xformOp:translate"]
}

```
</td> 
<td valign="top">

<img width="723" height="441" alt="image" src="https://github.com/user-attachments/assets/92dd571f-af7a-4987-b333-6394875d04ec" />

</td> 

</table>

##### ⭐ Example using Uniform Interpolation

<table>
<tr>
<th align="left">uniform.usda</th>
<th align="left">Result</th>
</tr>
<tr>
    
<td valign="top">

```py
#usda 1.0
(
)

def Mesh "uniform"
{
    float3[] extent = [(-1, 0, 0), (1, 1, 0)]
    point3f[] points = [(-1, 0, 0), (-1, 1, 0), (0, 1, 0), (0, 0, 0), (1, 1, 0), (1, 0, 0)]
    int[] faceVertexCounts = [4, 4]
    int[] faceVertexIndices = [3, 2, 1, 0, 5, 4, 2, 3]

    color3f[] primvars:displayColor = [(1, 0, 0), (0,0,1)] (
        interpolation = "uniform"
    )

    double3 xformOp:translate = (0, 0, -10)
    uniform token[] xformOpOrder = ["xformOp:translate"]
}

```
</td> 
<td valign="top">

<img width="686" height="399" alt="image" src="https://github.com/user-attachments/assets/0bb621ac-7e34-43ac-b3b1-024a9c50e58b" />


</td> 

</table>

##### ⭐ Example using vertex Interpolation

<table>
<tr>
<th align="left">vertex.usda</th>
<th align="left">Result</th>
</tr>
<tr>
    
<td valign="top">

```py
#usda 1.0
(
)

def Mesh "vertex"
{
    float3[] extent = [(-1, 0, 0), (1, 1, 0)]
    point3f[] points = [(-1, 0, 0), (-1, 1, 0), (0, 1, 0), (0, 0, 0), (1, 1, 0), (1, 0, 0)]
    int[] faceVertexCounts = [4, 4]
    int[] faceVertexIndices = [3, 2, 1, 0, 5, 4, 2, 3]

    color3f[] primvars:displayColor = [(1, 0, 0), (0.75,0,0), (0.5,0,0.25), (0.25,0,0.5), (0,0,1), (0,0,0.75)] (
        interpolation = "vertex"
    )

    double3 xformOp:translate = (0, 0, -10)
    uniform token[] xformOpOrder = ["xformOp:translate"]
}

```
</td> 
<td valign="top">

<img width="671" height="389" alt="image" src="https://github.com/user-attachments/assets/3d3526e7-fcf4-4788-9c2a-2f4bfa391b4f" />



</td> 

</table>

##### ⭐ Example using varying Interpolation

<table>
<tr>
<th align="left">varying.usda</th>
<th align="left">Result</th>
</tr>
<tr>
    
<td valign="top">

```py
#usda 1.0
(
)

def Mesh "varying"
{
    float3[] extent = [(-1, 0, 0), (1, 1, 0)]
    point3f[] points = [(-1, 0, 0), (-1, 1, 0), (0, 1, 0), (0, 0, 0), (1, 1, 0), (1, 0, 0)]
    int[] faceVertexCounts = [4, 4]
    int[] faceVertexIndices = [3, 2, 1, 0, 5, 4, 2, 3]

    color3f[] primvars:displayColor = [(1, 0, 0), (0.75,0,0), (0.5,0,0.25), (0.25,0,0.5), (0,0,1), (0,0,0.75)] (
        interpolation = "varying"
    )

    double3 xformOp:translate = (0, 0, -10)
    uniform token[] xformOpOrder = ["xformOp:translate"]
}

```
</td> 
<td valign="top">

<img width="629" height="328" alt="image" src="https://github.com/user-attachments/assets/7f7591e2-2212-41ec-a434-edd7e058f480" />



</td> 

</table>

Note: If you’re working with polygonal mesh data that is explicitly not intended to be subdivided, you should use varying interpolation in addition to setting the mesh subdivision scheme to none. This will ensure that the mesh renders identically whether a renderer supports subdivision or not.

##### ⭐ Example using faceVarying Interpolation

<table>
<tr>
<th align="left">faceVarying.usda</th>
<th align="left">Result</th>
</tr>
<tr>
    
<td valign="top">

```py
#usda 1.0
(
)

def Mesh "faceVarying"
{
    float3[] extent = [(-1, 0, 0), (1, 1, 0)]
    point3f[] points = [(-1, 0, 0), (-1, 1, 0), (0, 1, 0), (0, 0, 0), (1, 1, 0), (1, 0, 0)]
    int[] faceVertexCounts = [4, 4]
    int[] faceVertexIndices = [3, 2, 1, 0, 5, 4, 2, 3]

    color3f[] primvars:displayColor = [(0,0,1), (0,0,0.75), (0.75,0,0), (1,0,0),
                                       (0,0,1), (0,0,0.75), (0.75,0,0), (1,0,0)] (
        interpolation = "faceVarying"
    )

    double3 xformOp:translate = (0, 0, -10)
    uniform token[] xformOpOrder = ["xformOp:translate"]
}
```
</td> 
<td valign="top">

<img width="657" height="373" alt="image" src="https://github.com/user-attachments/assets/b0662cbb-2a6f-4675-9b26-98f3d22ed8a3" />



</td> 

</table>

Primvars have a characteristic different from most USD attributes in that primvars will get “inherited” down the scene namespace. Regular USD attributes only apply to the prim on which they are specified, but primvars implicitly also apply to all child imageable prims (unless the child prims have their own opinions about those primvars).

Primvar Element Size: sets how many consecutive values in the primvar array should be treated as a single element to be interpolated over a Gprim

##### ⭐ Example using Primvar Element Size

<table>
<tr>
<th align="left">elementsize.usda</th>
<th align="left">Flattened result</th>
</tr>
<tr>
    
<td valign="top">

```py
#usda 1.0
(
)

def Cube "TestPrim"
{
    string[] primvars:testPrimvar = ["element1-partA", "element1-partB", "element2-partA", "element2-partB"] (
        elementSize = 2
    )
    int[] primvars:testPrimvar:indices = [0, 1, 0]
}
```
</td> 
<td valign="top">
	
```py
	
	[element1-partA, element1-partB, element2-partA, element2-partB, element1-partA, element1-partB]


```
</td> 

</table>

Notice how the primvar indices refer to pairs of values in the value array – the “1” index refers to the third and fourth items in the values array.

Generally, the default element size of 1 will work for most use-cases. However you may encounter use-cases where you need to communicate an aggregate element to a renderer (e.g. representing spherical harmonics using nine floating-point coefficients) using larger element sizes.

If you want to dig much more in primvars and materials, follow the next doc.

🔗 [More info](https://openusd.org/release/user_guides/render_user_guide.html#working-with-primvars)


### 5.3.2- Value Resolution

Value resolution is how OpenUSD figures out the final value of a property or piece of metadata by looking at all the different sources that might have information about it.

Key Differences and Main Points: Value Resolution vs Composition in OpenUSD

| **Aspect**                          | **Value Resolution**                                                                 | **Composition**                                                                 |
|-------------------------------------|-------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| **Definition**                      | Determines the final value of a property or metadata by combining multiple sources. | Determines where data comes from and creates an index of sources for each prim. |
| **Caching**                         | Not cached; values are calculated on demand for efficiency and memory optimisation. | Cached at the prim level for quick access.                                      |
| **Rules**                           | Vary by data type (e.g., metadata, relationships, attributes).                      | Vary by composition arc and strength ordering.                                  |
| **Metadata Resolution**             | Strongest opinion wins; some metadata (e.g., dictionaries) combine element by element. | Strongest opinion wins based on composition arcs and strength ordering.         |
| **Relationship Resolution**         | Combines multiple targets using list editing semantics (e.g., merging lists).       | Determines the hierarchy and structure of the scene.                            |
| **Attribute Resolution**            | Considers value clips, time samples, and default values, with time scaling and interpolation. | Focuses on organising and layering data sources.                                |
| **Performance**                     | Optimised for runtime efficiency and low memory usage.                              | Pre-calculates composition logic for faster access.                             |
| **Key Use Case**                    | Combines data from multiple sources seamlessly in a non-destructive workflow.       | Organises and indexes data sources for efficient scene management.              |
| **Python Tools**                    | Use `UsdAttributeQuery` to cache attribute values for repeated access.              | No specific tools mentioned for caching.                                        |

##### 🐍 Example: Attribute Value Resolution and Animation

<table>
<tr>
<th align="left">Code</th>
<th align="left">light_props.usda</th>
</tr>
<tr>
    
<td valign="top">

```py
from pxr import Gf, Usd, UsdGeom, UsdLux

file_path = "_assets/light_props.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)
geom_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, "/Geometry")
cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, geom_scope.GetPath().AppendPath("Box"))

# Define a `Scope` Prim in stage at `/Lights`:
lights_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, "/Lights")

# Define a `Sun` prim in stage as a child of `lights_scope`, called `Sun`:
distant_light = UsdLux.DistantLight.Define(stage, lights_scope.GetPath().AppendPath("Sun"))
# Define a `SphereLight` prim in stage as a child of lights_scope called `SphereLight`:
sphere_light = UsdLux.SphereLight.Define(stage, lights_scope.GetPath().AppendPath("SphereLight"))

# Configure the distant light's emissive attributes:
distant_light.GetColorAttr().Set(Gf.Vec3f(1.0, 0.0, 0.0)) # Light color (red)
distant_light.GetIntensityAttr().Set(120.0) # Light intensity
# Lights are Xformable
if not (distant_light_xform_api := UsdGeom.XformCommonAPI(distant_light)):
    raise Exception("Prim not compatible with XformCommonAPI")
distant_light_xform_api.SetRotate((45.0, 0.0, 0.0))


# Configure the sphere light's emissive attributes:
sphere_light.GetColorAttr().Set(Gf.Vec3f(0.0, 0.0, 1.0)) # Light color (blue)
sphere_light.GetIntensityAttr().Set(50000.0) # Light intensity
# Lights are Xformable
if not (sphere_light_xform_api := UsdGeom.XformCommonAPI(sphere_light)):
    raise Exception("Prim not compatible with XformCommonAPI")
sphere_light_xform_api.SetTranslate((5.0, 10.0, 0.0))

stage.Save()


```
</td> 
<td valign="top">

```py
#usda 1.0
(
    defaultPrim = "World"
    endTimeCode = 120
    startTimeCode = 1
    timeCodesPerSecond = 30
)

def Xform "World"
{
    float3 xformOp:rotateXYZ = (-75, 0, 0)
    uniform token[] xformOpOrder = ["xformOp:rotateXYZ"]

    def Cube "Ground"
    {
        float3 xformOp:scale = (10, 5, 0.1)
        double3 xformOp:translate = (0, 0, -0.1)
        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:scale"]
    }

    def Cube "StaticDefaultCube"
    {
        color3f[] primvars:displayColor = [(0.2, 0.2, 0.8)]
        float3 xformOp:scale
        double3 xformOp:translate = (8, 0, 1)
        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:scale"]
    }

    def Cube "StaticCube"
    {
        color3f[] primvars:displayColor = [(0.8, 0.2, 0.2)]
        float3 xformOp:scale = (1.5, 1.5, 1.5)
        double3 xformOp:translate = (-8, 0, 1.5)
        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:scale"]
    }

    def Cube "AnimCube"
    {
        color3f[] primvars:displayColor = [(0.2, 0.8, 0.2)]
        float3 xformOp:scale = (1.5, 1.5, 1.5)
        float3 xformOp:scale.timeSamples = {
            60: (2.5, 2.5, 2.5),
            120: (5, 5, 5),
        }
        double3 xformOp:translate = (0, 0, 1.5)
        double3 xformOp:translate.timeSamples = {
            60: (0, 0, 2.5),
            120: (0, 0, 5),
        }
        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:scale"]
    }
}



```
</td> 

</table

##### 🐍 Example: 

<table>
<tr>
<th align="left">Code</th>
<th align="left">value_resolution_composed.usda</th>
</tr>
<tr>
    
<td valign="top">

```py
from pxr import Usd, UsdGeom
import os

# --- Layer 1 (weaker)
layer_1_path = "_assets/value_resolution_layer_1.usda"
layer_1_stage = Usd.Stage.CreateNew(layer_1_path)

layer_1_xform = UsdGeom.Xform.Define(layer_1_stage, "/World/XformPrim")
layer_1_xform_prim = layer_1_xform.GetPrim()

# "/World/XformPrim" customData
layer_1_xform_prim.SetCustomDataByKey("source",  "layer_1")
layer_1_xform_prim.SetCustomDataByKey("opinion",  "weak")
layer_1_xform_prim.SetCustomDataByKey("unique_layer_value", "layer_1_unique_value")  # only authored in layer_1

# Relationship contribution from base
look_a = UsdGeom.Xform.Define(layer_1_stage, "/World/Looks/LookA")
layer_1_xform_prim.CreateRelationship("look:targets").AddTarget(look_a.GetPath())
layer_1_stage.Save()

# --- Layer 2 (stronger)
layer_2_path = "_assets/value_resolution_layer_2.usda"
layer_2_stage = Usd.Stage.CreateNew(layer_2_path)

layer_2_xform = UsdGeom.Xform.Define(layer_2_stage, "/World/XformPrim")
layer_2_xform_prim = layer_2_xform.GetPrim()

# "/World/XformPrim" customData
layer_2_xform_prim.SetCustomDataByKey("source",  "layer_2")
layer_2_xform_prim.SetCustomDataByKey("opinion",  "strong")

# Relationship contribution from override
look_b = UsdGeom.Xform.Define(layer_2_stage, "/World/Looks/LookB")
layer_2_xform_prim.CreateRelationship("look:targets").AddTarget(look_b.GetPath())
layer_2_stage.Save()

# --- Composed stage. First sublayer listed (layer_2) is strongest
composed_path = "_assets/value_resolution_composed.usda"
composed_stage = Usd.Stage.CreateNew(composed_path)
composed_stage.GetRootLayer().subLayerPaths = [os.path.basename(layer_2_path), os.path.basename(layer_1_path)]

xform_prim = composed_stage.GetPrimAtPath("/World/XformPrim")
resolved_custom_data = xform_prim.GetCustomData() 

# resolved custom data:
print("Resolved CustomData:")
for key, value in resolved_custom_data.items():
    print(f"- '{key}': '{value}'")

# resolved relationship targets:
targets = xform_prim.GetRelationship("look:targets").GetTargets()
print(f"\nResolved relationship targets: {[str(t) for t in targets]}")  # both LookA and LookB

composed_stage.Save()

# Write out the composed stage to a single file for inspection
explicit_composed_path = '_assets/value_resolution_composed_explicit.usda'
txt = composed_stage.ExportToString(addSourceFileComment=False)
with open(explicit_composed_path, "w") as f:
    f.write(txt)


```
</td> 
<td valign="top">

```py
#usda 1.0

def "World"
{
    def Xform "XformPrim" (
        customData = {
            string opinion = "strong"
            string source = "layer_2"
            string unique_layer_value = "layer_1_unique_value"
        }
    )
    {
        custom rel look:targets = [
            </World/Looks/LookB>,
            </World/Looks/LookA>,
        ]
    }

    def "Looks"
    {
        def Xform "LookA"
        {
        }

        def Xform "LookB"
        {
        }
    }
}



```
</td> 

</table>

**List Editing**

---

List editing is a USD feature that allows array-valued elements to be non-destructively and sparsely modified across composition layers, instead of being fully overridden. This enables layered workflows where stronger layers adjust lists defined in weaker layers without copying or rewriting them.

Supported List Operations:

| Operation            | Description                                    | Behavior                                              |
| -------------------- | ---------------------------------------------- | ----------------------------------------------------- |
| **append**           | Add value(s) to the end of the resolved list   | Existing values are reshuffled to the back            |
| **prepend**          | Add value(s) to the front of the resolved list | Existing values are reshuffled to the front           |
| **delete**           | Remove value(s) from the resolved list         | Safe and speculative; no error if value doesn’t exist |
| **explicit (reset)** | Replace the entire resolved list               | Ignores all weaker-layer list operations              |

| Rule                     | Explanation                                                         |
| ------------------------ | ------------------------------------------------------------------- |
| Non-destructive          | Weaker layers remain intact                                         |
| Sparse                   | Only changes are authored                                           |
| Order-aware              | Prepend and append affect ordering                                  |
| Layer-dependent strength | Prepending in weaker layers can override appends in stronger layers |
| No duplication           | Resolved lists behave like sets                                     |
| No repetition in ops     | Same value cannot appear twice in one operation                     |

| Syntax                     | Meaning                              |
| -------------------------- | ------------------------------------ |
| `references = @file.usd@`  | Explicit reset                       |
| `references += @file.usd@` | Append                               |
| `references -= @file.usd@` | Delete                               |
| Single value allowed       | Brackets optional for single entries |
| Multiple values            | Use `[ ... ]` list syntax            |



### 5.3.3- Custom Properties

Here are a few ways we can use custom properties to enhance our OpenUSD workflows:

- Metadata storage : Storing additional information about a prim, such as author names, creation dates, or custom tags.
- Animation data : Defining custom animation curves or parameters that are not covered by standard schema properties.
- Simulation parameters : Storing parameters for physics simulations or other procedural generation processes.
- Arbitrary end user data : Because they can be easily defined at run time, custom properties are the best way to allow end users to define arbitrary custom data.

##### 🐍 Example: Creating Custom Attributes

<table>
<tr>
<th align="left">Code</th>
<th align="left">custom_attributes.usda</th>
</tr>
<tr>
    
<td valign="top">

```py
from pxr import Usd, UsdGeom, Sdf

file_path = "_assets/custom_attributes.usda"
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)

world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
geometry_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, world_xform.GetPath().AppendPath("Packages"))

box_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, geometry_xform.GetPath().AppendPath("Box"))
box_prim: Usd.Prim = box_xform.GetPrim()
box_prim.GetReferences().AddReference("./cubebox_a02/cubebox_a02.usd")

# Create additional attributes for the box prim
weight = box_prim.CreateAttribute("acme:weight", Sdf.ValueTypeNames.Float, custom=True)
category = box_prim.CreateAttribute("acme:category", Sdf.ValueTypeNames.String, custom=True)
hazard = box_prim.CreateAttribute("acme:hazardous_material", Sdf.ValueTypeNames.Bool, custom=True)

# Optionally document your custom property
weight.SetDocumentation("The weight of the package in kilograms.")
category.SetDocumentation("The shopping category for the products this package contains.")
hazard.SetDocumentation("Whether this package contains hazard materials.")

# Set values for the attributes
weight.Set(5.5)
category.Set("Cosmetics")
hazard.Set(False)

# Save the stage
stage.Save()


```
</td> 
<td valign="top">

```py
#usda 1.0

def Xform "World"
{
    def Xform "Packages"
    {
        def Xform "Box" (
            prepend references = @./cubebox_a02/cubebox_a02.usd@
        )
        {
            custom string acme:category = "Cosmetics" (
                doc = "The shopping category for the products this package contains."
            )
            custom bool acme:hazardous_material = 0 (
                doc = "Whether this package contains hazard materials."
            )
            custom float acme:weight = 5.5 (
                doc = "The weight of the package in kilograms."
            )
        }
    }
}


```
</td> 

</table>



##### 🐍 Example: Modifying Custom Attributes

<table>
<tr>
<th align="left">Code</th>
<th align="left">custom_attributes.usda</th>
</tr>
<tr>
    
<td valign="top">

```py
from pxr import Usd

file_path = "_assets/custom_attributes.usda"
stage: Usd.Stage = Usd.Stage.Open(file_path)
box_prim = stage.GetPrimAtPath("/World/Packages/Box")

# Get the weight attribute
weight_attr: Usd.Attribute = box_prim.GetAttribute("acme:weight")
# Set the value of the weight attribute
weight_attr.Set(4.25)

# Print the weight of the box
print("Weight of Box:", weight_attr.Get())

stage.Save()


```
</td> 
<td valign="top">

```py
#usda 1.0

def Xform "World"
{
    def Xform "Packages"
    {
        def Xform "Box" (
            prepend references = @./cubebox_a02/cubebox_a02.usd@
        )
        {
            custom string acme:category = "Cosmetics" (
                doc = "The shopping category for the products this package contains."
            )
            custom bool acme:hazardous_material = 0 (
                doc = "Whether this package contains hazard materials."
            )
            custom float acme:weight = 4.25 (
                doc = "The weight of the package in kilograms."
            )
        }
    }
}


```
</td> 

</table>

🔗 [More info](https://docs.nvidia.com/learn-openusd/latest/beyond-basics/custom-properties.html)

### 5.3.4- Active and Inactive Prims

Deactivating a prim provides a way to temporarily remove, or prune, prims and their descendants from being composed and processed on the stage, which can make traversals more efficient.

##### 🐍 Example: Setting Prims as Active/Inactive

<table>
<tr>
<th align="left">Code</th>
<th align="left">Result</th>
</tr>
<tr>
    
<td valign="top">

```py
from pxr import Usd

# Open the USD stage from the specified file
file_path = "_assets/active-inactive.usda"
stage = Usd.Stage.Open(file_path)

# Iterate through all the prims on the stage
# Print the state of the stage before deactivation
print("Stage contents BEFORE deactivating:")
for prim in stage.Traverse():
    print(prim.GetPath())

# Get the "/World/Box" prim and deactivate it
box = stage.GetPrimAtPath("/World/Box")
# Passing in False to SetActive() will set the prim as Inactive and passing in True will set the prim as active
box.SetActive(False)

print("\n\nStage contents AFTER deactivating:")
for prim in stage.Traverse():
    print(prim.GetPath())


```
</td> 
<td valign="top">

```py
Stage contents BEFORE deactivating:
/World
/World/Box
/World/Box/Geometry
/World/Box/Geometry/Cube
/World/Box/Materials
/World/Box/Materials/BoxMat
/World/Environment
/World/Environment/SkyLight


Stage contents AFTER deactivating:
/World
/World/Environment
/World/Environment/SkyLight


```
</td> 

</table>

### 5.3.5- Model Kinds -> (go to 2.1)
### 5.3.6- Stage Traversal -> (go to 2.2)
### 5.3.7- Hydra

Hydra is a rendering architecture within OpenUSD that provides a high-performance, scalable, and extensible solution for rendering large 3D scenes. It serves as a bridge between the scene description data, such as USD, and the rendering backend, such as OpenGL or DirectX.
Hydra is a rendering architecture within OpenUSD that bridges scene data and rendering backends.
It operates on a scene delegate and enables render delegate plugins to generate rendering instructions for specific backends.
Hydra supports various rendering backends and techniques, including rasterization and ray tracing.
It provides extensibility through plugins and custom rendering backends.

🔗 [More info](https://docs.nvidia.com/learn-openusd/latest/beyond-basics/hydra.html)


# 6) Debugging and Troubleshooting: Exam Weight 11%

## 6.0 Related Topics already explored

- Traversing a Stage -> (go to 2.2)
- LIVERPS -> (go to 1.7)
- References -> (go to 1.2.5)
- ISA Schemas -> (go to 3.1)
- Inherits -> (go to 1.2.2)
- USDCAT -> (go to 4.5)

## 6.1 Creating Composition Arcs -> (go to 1.1 - 1.2)

## 6.2 Inspecting and Authoring Properties

##### 🐍 Example: Inspecting and Authoring Properties

<table>
<tr>
<th align="left">Code</th>
<th align="left">.usda</th>
</tr>
<tr>
    
<td valign="top">

```py

# To run From Script Editor in Omniverse

from pxr import Usd, UsdGeom, Sdf
from omni.usd import get_context

stage = get_context().get_stage()

world_prim = stage.GetPrimAtPath("/World")

if not world_prim.IsValid():
    world_xform = UsdGeom.Xform.Define(stage, "/World")
else:
    world_xform = UsdGeom.Xform(world_prim)
    
    geometry_xform = UsdGeom.Sphere.Define(stage, "/World/Sphere")

from pxr import Usd, UsdGeom, Sdf
from omni.usd import get_context

stage = get_context().get_stage()

world_prim = stage.GetPrimAtPath("/World")

if not world_prim.IsValid():
    world_xform = UsdGeom.Xform.Define(stage, "/World")
else:
    world_xform = UsdGeom.Xform(world_prim)
    
    geometry_xform = UsdGeom.Sphere.Define(stage, "/World/Sphere")


```
</td> 
<td valign="top">

```py
#usda 1.0
(
    defaultPrim = "World"
    endTimeCode = 1000000
    metersPerUnit = 1
    startTimeCode = 0
    timeCodesPerSecond = 60
    upAxis = "Z"
)

def Xform "World"
{
    def Sphere "Sphere"
    {
        float3[] extent = [(-2, -2, -2), (2, 2, 2)]
        color3f[] primvars:displayColor = [(0, 0, 1)]
        double radius = 2
    }
}


```
</td> 

</table>

##### 🧠 [Tutorial] (https://openusd.org/release/tut_inspect_and_author_props.html) - [Material] (https://github.com/DreamCodes4Life/OpenUSDFundamentals/tree/main/tutorials/authoringProperties)

## 6.3 Visibility

Visibility is a builtin attribute of the UsdGeomImageable base schema, and models the simplest form of “pruning” invisibility that is supported by most DCC apps. Visibility can take on two possible token string values:

inherited (the fallback value if the attribute is not authored)

invisible

If the resolved value is invisible, then neither the prim itself nor any prims in the subtree rooted at the prim should be rendered - this is what we mean by “pruning invisibility”, since invisible subtrees are definitively pruned in their entirety. If the resolve value is inherited, it means that the computed visibility (as provided by UsdGeomImageable::ComputeVisibility()) of the prim will be whatever the computed value of the prim’s namespace parent is.

Visibility may be animated, allowing a sub-tree of geometry to be renderable for some segment of a shot, and absent from others; unlike the action of deactivating geometry prims, invisible geometry is still available for inspection, for positioning, for defining volumes, etc.

## 6.4 USD Performance

OpenUSD Performance Cheat Sheet

Practical notes distilled from the official “Maximizing Performance” docs.

You’re likely hitting avoidable performance bottlenecks if you notice any of these:

- Stage open time grows **much faster than linearly** with scene size.
- Hydra / viewport feels sluggish when loading or switching shots.
- Tools that make **many USD edits** (imports, retimes, mass metadata updates) get slow as scenes grow.
- Assets are made up of **many tiny layers** or very large `.usda` files.

---

### Key Practices

| Topic | When It Matters (Symptoms) | What To Do |
| ----- | -------------------------- | ---------- |
| **Use a multithreaded allocator** | CPU usage looks high but scaling across cores is poor; loading big stages or imaging is slower than expected on many-core machines. | Link USD (and your DCC host if possible) against a multithread-friendly allocator such as **jemalloc**. This often gives ~2× speed-ups for multi-core workloads. On Linux, you can experiment by `LD_PRELOAD`-ing jemalloc when launching your app. |
| **Prefer binary `.usd` (usdc) for heavy data** | Large text `.usda` files take a long time to open; memory usage is high; Alembic-to-USD conversions feel heavy. | Store geometry and animation caches in **binary crate** files (`.usd` / `usdc`). Reserve `.usda` mainly for small, human-readable “interface” layers (asset info, variants, payload wiring). Convert heavy `.usda` or Alembic to `.usd` where possible. |
| **Package assets with payloads** | Opening a full shot composes all geometry and shading at once, making first-open very slow; even just inspecting the scene graph is expensive. | Use **payloads** to separate a lightweight “interface” layer (model prim, asset info, variants, bbox) from heavier detail (geo, materials, animation). Open stages **unloaded** and load only the prims you actually need. |
| **Keep layer counts reasonable** | Each asset is made of many small layers (e.g., 10+), multiplied across all references and instances, causing lots of I/O and composition work. | Treat “lots of layers per asset” as a smell. Flatten or stitch authoring/workflow layers into a smaller set at publish time. Use tools like `usdcat --flatten` and friends, and keep an eye on `UsdStage::GetUsedLayers()`. |
| **Minimize prim count (vs. property count)** | Stage open time grows sharply with the number of prims, even when you don’t add much more data per prim. | Spend your “budget” on **fewer prims with more properties**, not more prims. Avoid extra hierarchy prims that exist only for organization; use **namespaced properties** instead where possible. |
| **Avoid unnecessary Xform+gprim pairs** | Lots of tiny `Xform` + `Mesh` pairs everywhere; prim count goes through the roof for complex scenes. | Use transformable gprims: in many cases you can transform the gprim itself instead of adding an extra `Xform` parent. This can significantly cut prim count (often 40–50% in dense scenes). |
| **Use instancing at the right level** | You have many repeated objects, but performance is still bad despite “instancing” everything at the gprim level. | Prefer instancing **at asset / collection level** instead of per-gprim. Fine-grained instancing alone doesn’t reduce prim count and can add composition overhead; coarser instancing reduces both memory and composition work. |

---

### SdfChangeBlock & Bulk Edits

When doing **many edits to layers or specs in a loop** (C++ or Python), change notifications and cache invalidation can dominate cost.

Use `SdfChangeBlock` when:

- You’re importing, retiming, or mass-editing **thousands of specs**.
- You **don’t** need observers (like a UI) to see each individual intermediate change.
- You conceptually care about the **final state** of the edits, not each step.


## 6.5 Over vs typeless

def means “Even though I may not be declaring a typed prim in this layer, by the time the UsdStage has finished composing, I expect a type to have been provided by referenced/layered scene description” (in the example, presumably the type would be provided by the layer targeted by the payload arc.

over means “If some referenced layer happens to define this prim, then layer the information I contain onto it; but if not, just consider this information ancillary”

## 6.6 Draw Modes

## UsdGeomModelAPI – Draw Modes (Simple Summary)

`UsdGeomModelAPI` adds **draw modes** that let you replace heavy geometry with simple stand-ins in the viewport for prims of `kind = model`. :contentReference[oaicite:0]{index=0}  

Two key attributes control this:

- **`model:drawMode`** (inheritable) – says *what kind* of stand-in to use (origin, bounds, cards, etc.). :contentReference[oaicite:1]{index=1}  
- **`model:applyDrawMode`** (not inherited) – a boolean that says *whether to actually use* the resolved draw mode on this prim. :contentReference[oaicite:2]{index=2}  

USD can then **stop traversing the subtree** at that prim and draw proxy geometry instead (axes, bounding box, or textured “cards”). This is mainly for performance + clarity when looking at big scenes. :contentReference[oaicite:3]{index=3}  

For `kind = component` models, if you *do not* author `model:applyDrawMode`, they behave as if it were `true` when `model:drawMode` resolves to a non-`default` value. If you want to **opt-out**, apply `UsdGeomModelAPI` and explicitly set `model:applyDrawMode = false`. :contentReference[oaicite:4]{index=4}  

`cards` mode uses flat quads around the model, with textures and layout controlled by `model:cardGeometry` and per-axis texture attributes (X/Y/Z ±). :contentReference[oaicite:5]{index=5}  

---

### Draw Mode Attributes Cheat Sheet

| Attribute | Type / Scope | What It Does | Common Values / Notes |
| ---------- | ------------ | ------------ | ---------------------- |
| **`model:drawMode`** | token, **inherited** | Chooses the *type* of proxy geometry when draw mode is applied. | **`origin`** – draw basis vectors at the prim’s origin. **`bounds`** – draw the model-space bounding box. **`cards`** – draw textured quads as a stand-in. **`default`** – draw the full USD subtree normally. **`inherited`** – defer to parent’s drawMode; if nothing is set anywhere, result is `default`. :contentReference[oaicite:6]{index=6} |
| **`model:applyDrawMode`** | bool, **not inherited** | Controls whether this prim actually uses the resolved `model:drawMode`. | If `true` and resolved `model:drawMode` is not `default`, USD stops traversal here and draws proxy geometry. For `kind = component`, “no opinion authored” is treated as `true` by default. Set to `false` to force full geometry even when a non-default drawMode is inherited. :contentReference[oaicite:7]{index=7} |
| **`model:drawModeColor`** | color3f, not inherited | Base color for generated proxy geometry (axes, bounds lines, or untextured cards). | Default is a mid-gray; used when no texture exists or when a card face has an invalid texture path. :contentReference[oaicite:8]{index=8} |
| **`model:cardGeometry`** | token, not inherited | Controls the **shape** of the quads in `cards` mode. | **`cross`** – quads that bisect the model along ±X, ±Y, ±Z. **`box`** – quads on the faces of the bounds box. **`fromTexture`** – quads and placement taken from texture metadata (world-to-screen matrix). :contentReference[oaicite:9]{index=9} |
| **`model:cardTextureXPos`**<br>`model:cardTextureXNeg`<br>`model:cardTextureYPos` / `YNeg`<br>`model:cardTextureZPos` / `ZNeg` | asset paths, not inherited | Textures used on each axis-aligned card face in `cards` mode. | If both + and − textures exist on an axis, each side uses its own. If only one is set, it’s mirrored (flipped in s) to the opposite side. Faces with missing/invalid textures use `model:drawModeColor`. In `fromTexture` mode, only faces with valid textures are drawn. :contentReference[oaicite:10]{index=10} |

---

### How It All Fits Together (Short Version)

1. Set `model:drawMode` somewhere up the hierarchy (`origin`, `bounds`, or `cards`).  
2. On the prim where you want the proxy to actually be used, ensure `model:applyDrawMode = true` (or rely on the component default).  
3. Optionally: adjust `model:drawModeColor`, `model:cardGeometry`, and the card textures for nicer impostors. :contentReference[oaicite:11]{index=11}  

That’s enough to get simple, efficient stand-in rendering for your models using `UsdGeomModelAPI`’s draw modes.






# 7) Pipeline Development: Exam Weight 14%




# 8) Visualization: Exam Weight 8%
















##### ⭐ Example
##### 🐍 Example: 

<table>
<tr>
<th align="left"></th>
<th align="left"></th>
</tr>
<tr>
    
<td valign="top">

```py



```
</td> 
<td valign="top">

```py



```
</td> 

</table>




https://docs.nvidia.com/learn-openusd/latest/stage-setting/properties/attributes.html
