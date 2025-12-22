## 🎯 Creating Composition Arcs

**Composition arcs** are operators that allow **USD** to combine multiple layers of scene description in specific ways.

---

### 🧠 The 7 Composition Arc Types (LIVERPS)

Ordered by **strength (weak → strong)**:

| Order | Arc Type | Description |
|-----|---------|------------|
| L | **Link** | Internal connections |
| I | **Inherit** | Share opinions from a base prim |
| V | **Variant Set** | Switchable configurations |
| E | **Relocate** | Move prim paths |
| R | **Reference** | Bring in external USD |
| P | **Payload** | Lazy-loaded references |
| S | **Specialize** | Stronger form of inheritance |

> **Mnemonic:** **LIVERPS** — strength ordering for composition arcs

---

### 📦 Sublayer (Local)

**Sublayer** is the *only* composition arc that **does NOT support prim name changes**.

Key properties:
- Applies to **all sublayers in the root layer’s LayerStack**
- Direct opinions from *every sublayer* are consulted
- Often used to assemble shots and sequences

---

### 🗂️ Example: Shot → Sequence Composition

#### `shot.usd`
```usda
#usda 1.0
(
    subLayers = [
        @shotFX.usd@,
        @shotAnimationBake.usd@,
        @sequence.usd@
    ]
)
