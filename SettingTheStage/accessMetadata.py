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