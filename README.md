Creating Composition Arcs
Composition arcs are the operators that allow USD to combine multiple layers of scene description in specific ways.
Seven types of composition arcs (LIVERPS for Strenght Ordering): Link
Sublayer (local) - inherit  - variant set  - r(E)locates - reference - payload – specialize
Sublayer (local): The only one that don’t support support prim name changes. This is where the effect of direct opinions in all SubLayers of the root layer of the LayerStack will be consulted
shot.usd	sequence.usd
#usda 1.0
(
    subLayers = [
        @shotFX.usd@,
        @shotAnimationBake.usd@,
        @sequence.usd@
    ]
)
	#usda 1.0
(
    subLayers = [
        @sequenceFX.usd@,
        @sequenceLayout.usd@,
        @sequenceDressing.usd@
    ]
)

