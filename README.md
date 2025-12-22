# Composition: Exam Weight 23%

<p align="center">
  <strong>Authoring, design with, or debugging composition arcs. A developer needs to know all of the composition arcs, how they
work, and when and when it is appropriate to use each. The developer needs to be able to debug complex LIVRPS scenarios</strong>
</p>

---

##  Creating Composition Arcs

**Composition arcs** are the operators that allow **USD (Universal Scene Description)** to combine multiple layers of scene description in specific ways.

They define **how opinions are discovered, ordered, and resolved** across multiple files and layers.

---

##  The 7 Composition Arc Types (LIVERPS)

Composition arcs are evaluated according to **strength ordering** (from weakest → strongest).

| Order | Arc Type | Purpose |
|-----|---------|--------|
| L | **Link** | Connect internal relationships |
| I | **Inherit** | Share properties from a base prim |
| V | **Variant Set** | Enable configuration switching |
| E | **Relocate** | Move prim paths |
| R | **Reference** | Bring in external USD layers |
| P | **Payload** | Lazy-load external content |
| S | **Specialize** | Stronger form of inheritance |

> **Mnemonic:** **LIVERPS** — the strength ordering of composition arcs

---

## 📦 Sublayer (Local)

**Sublayer** is a special composition mechanism:

- It **does not support prim name changes**
- It applies to **all sublayers in the root layer’s LayerStack**
- Direct opinions from *every sublayer* are consulted
- Commonly used for **shot, sequence, and asset assembly**

This makes sublayers ideal for **non-destructive layering** of work from multiple departments.

---

##  Example: Shot → Sequence Composition

The following example shows how a **shot** composes multiple layers and includes an entire **sequence**, which itself is composed of additional layers.

<table>
<tr>
<th align="left">shot.usd</th>
<th align="left">sequence.usd</th>
</tr>
<tr>
    
<td>
    
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
</td> <td>

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
</table>

## ⏱️ Layer Offsets for TimeSamples

**Layer offsets** allow TimeSamples to be **shifted and scaled** when a layer is brought in via **Sublayers or References**.

They are commonly used to:
- Retime animation clips
- Reuse animation data non-destructively
- Align animation in time without modifying the source layer

---

<table>
<tr>
<th align="left">shot.usd</th>
<th align="left">sequence.usd</th>
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
</td> <td>

```usda
This USD will resolve as next:
A timesample of 30 in the someAnimation will be resolved here at: 30*0.5 + 10 = 25.
Layer offsets cannot themselves vary over time
```



# Content Aggregation: Exam Weight 10%
# Customizing USD: Exam Weight 6%


