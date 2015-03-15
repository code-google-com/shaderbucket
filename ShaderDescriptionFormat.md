# Example File #
```
<?xml version="1.0" encoding="UTF-8"?>
<!-- simple shader -->
<shader name="Simple Shader" icon="simple.png" file="simple.sdl">

	<!-- a textual description of the shader -->
	<description>Simple test shader example for ShaderBuddy.</description>
		
	<!-- example colour parameter -->
	<parameter name="baseColour" type="colour" help="Base colour." default="0.18,0.18,0.18" />
	
	<!-- example float param -->
	<parameter name="basicFloat" type="float" help="Floating point value." default="0.5" />
		
	<!-- a group of shader parameters -->
	<group name="Texturing" expand="false">
		
		<!-- a checkbox -->
		<parameter name="useTextures" label="Enable" type="bool" help="Turns texturing on/off." default="true" />
			
		<!-- a seperator -->
		<seperator />
			
		<!-- a file string -->
		<parameter name="textureFile" label="Texture File" type="file" help="Filename for the base texture." default="" />
			
	</group>
	<!-- end group -->
		
</shader>
<!-- end shader -->
```