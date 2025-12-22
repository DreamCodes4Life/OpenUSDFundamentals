<img width="1458" height="442" alt="image" src="https://github.com/user-attachments/assets/cb3be4e7-cf02-4dfc-820d-7594be455aae" />

🔗 [Exam Guide](https://nvdam.widen.net/s/6kxsqcsrrw/ncp-openusd-development-study-guide)

# 1) Composition: Exam Weight 23%

<p align="left">
  <strong>Authoring, design with, or debugging composition arcs. A developer needs to know all of the composition arcs, how they
work, and when and when it is appropriate to use each. The developer needs to be able to debug complex LIVRPS scenarios</strong>
</p>

🔗 [More info](https://openusd.org/release/glossary.html#liverps-strength-ordering)

---

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

##### ⭐ Example: Shot → Sequence Composition

The following example shows how a **shot** composes multiple layers and includes an entire **sequence**, which itself is composed of additional layers.

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

##### ⭐ Example: Sublayers Simple example

The following example shows how a **shot** composes multiple layers and includes an entire **sequence**, which itself is composed of additional layers.

<table>
<tr>
<th align="left">sublayers_simple.usd</th>
<th align="left">sublayerA.usd</th>
<th align="left">sublayerB.usd</th>
</tr>
<tr>
    
<td valign="top">
    
```usda
#usda 1.0
(
    defaultPrim = "World"
    endTimeCode = 100
    metersPerUnit = 0.01
    startTimeCode = 0
    subLayers = [
        @./sublayerB.usd@,
        @./sublayerA.usd@
    ]
    timeCodesPerSecond = 24
    upAxis = "Y"
)

def Xform "World"
{
    def Scope "Geometry"
    {
    }
}


```
</td> 
<td valign="top">

```usda
#usda 1.0
(
    upAxis = "Y"
)

over "World"
{
    over "Geometry"
    {
        def Cube "Cube"
        {
            float3[] extent = [(-50, -50, -50), (50, 50, 50)]
            double size = 100
            double3 xformOp:rotateXYZ = (0, 0, 0)
            double3 xformOp:scale = (1, 1, 1)
            double3 xformOp:translate = (0, 0, 0)
            uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:rotateXYZ", "xformOp:scale"]
        }
    }
}
```
</td>
<td valign="top">

```usda
#usda 1.0
(
    upAxis = "Y"
)

over "World"
{
    over "Geometry"
    {
        def Sphere "Sphere"
        {
            float3[] extent = [(-50, -50, -50), (50, 50, 50)]
            double radius = 50
            custom bool refinementEnableOverride = 1
            custom int refinementLevel = 2
            double3 xformOp:rotateXYZ = (0, 0, 0)
            double3 xformOp:scale = (1, 1, 1)
            double3 xformOp:translate = (0, 150, 0)
            uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:rotateXYZ", "xformOp:scale"]
        }

        over "Cube"
        {
            double3 xformOp:translate = (0, 50, 0)
        }
    }
}


```
</td>

</table>


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

## Important concepts 

•	**PrimSpec** is a container for property data and nested PrimSpecs.

•	composition arcs can only be applied on PrimSpecs

•	A **PrimStack** is a list of PrimSpecs that contribute opinions for a composed prim’s metadata.

•	A **primvar** is a special attribute that a renderer associates with a geometric primitive, and can vary (interpolate) the value of the attribute over the surface/volume of the primitive

•	Composition is cached, value resolution is not

•	Composition is internally multi-threaded, value resolution is meant to be client multi-threaded. USD’s primary guidance for clients wishing to maximize USD’s performance on multi-core systems is to perform as much simultaneous value resolution and data extraction as possible

•	Composition rules vary by composition arc, value resolution rules vary by metadatum.

•	An **index**, also referred to as a PrimIndex, is the result of composition. A prim’s index contains an ordered (from strongest to weakest) list of “Nodes”. All of the queries on USD classes except for stage-level metadata rely on prim indices to perform value resolution.

# 2) Content Aggregation: Exam Weight 10%
# 3) Customizing USD: Exam Weight 6%
# 4) Data Exchange: Exam Weight 15%
# 5) Data Modeling: Exam Weight 13%
# 6) Debugging and Troubleshooting: Exam Weight 11%
# 7) Pipeline Development: Exam Weight 14%
# 8) Visualization: Exam Weight 8%















