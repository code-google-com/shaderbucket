ShaderBucket is a palette and appearance manager for renderman shaders.

# Concepts #

## Shader ##
A **shader** is a description of a renderman shader including it's parameters.
## Appearance ##
An **appearance** is an instance of a renderman shader. Several appearances with different parameters can be created from a common shader.
## Look ##
A **look** is the combination of one or more appearances
## Assignment ##
An **assignment** is the relationship between a **look** and the objects to which it's applied.
## Palette ##
A **palette** is a collection of appearances, looks and assignments. A **palette** can also contain other palettes.

# File Specifications #
  * [ShaderBucket Configuration](ConfigurationFileFormat.md)
  * [Shader Description](ShaderDescriptionFormat.md)
  * [Palette Description](PaletteDescriptionFormat.md)

# Environment Variables #
ShaderBucket can use certain environment variables for further configuration.
  * _$SHADERBUCKET\_PALETTE\_PATH_
  * _$SHADERBUCKET\_SHADER\_PATH_
  * _$SHADERBUCKET\_CONFIG\_FILE_