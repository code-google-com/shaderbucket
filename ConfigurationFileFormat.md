The configuration file is used to setup certain aspects of ShaderBucket.

# Settings #
## renderer ##
This setting is used to specify the command used to trigger renderman renders.
```
<setting name="renderer">renderdl</setting>
```

## previewrib ##
```
<setting name="previewrib">/path/to/preview/rib</setting>
```

## shaderpath ##
This setting is used to add default shader paths to be loaded with ShaderBucket. The path should contain shader description files in the **shd** file format. This setting can be called multiple times.
```
<setting name="shaderpath">/some/shader/path/here</setting>
```

## palettepath ##
This setting is used to add default palette paths to be loaded with ShaderBucket. The path should contain palette description files in the **plt** file format. This setting can be called multiple times.
```
<setting name="palettepath">/some/palette/path/here</setting>
```

# Example File #
```
<?xml version="1.0" encoding="UTF-8"?>

<!-- example configuration file -->
<configuration version="1">
    <setting name="renderer">renderdl</setting>
    <setting name="previewrib">share/rib/preview.rib</setting>
    <setting name="shaderpath">test/shaders</setting>
    <setting name="palettepath">test/palettes<setting>
</configuration>
<!-- end configuration -->
```