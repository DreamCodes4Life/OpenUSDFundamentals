from pxr import Usd, UsdGeom, UsdLux, UsdPhysics, Gf, Sdf

# Here’s an example where we’re creating a custom attribute to add a serial number and last maintenance date to a prim, 
# so a supervisor can easily identify which machines are due for maintenance from the 3D model.

stage = Usd.Stage.CreateInMemory()
prim = stage.DefinePrim("/ExamplePrim", "Xform")
serial_num_attr = prim.CreateAttribute("my_namespace:serial_number", Sdf.ValueTypeNames.String, custom=True)

assert serial_num_attr.IsCustom()

mtce_date_attr = prim.CreateAttribute("my_namespace:maintenance_date", Sdf.ValueTypeNames.String, custom=True)
serial_num_attr.Set("qt6hfg23")
mtce_date_attr.Set("20241004")

print(f"Serial Number: {serial_num_attr.Get()}")
print(f"Last Maintenance Date: {mtce_date_attr.Get()}")