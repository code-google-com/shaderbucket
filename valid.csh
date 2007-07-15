#!/bin/tcsh -f

# validate schemas
foreach file (`ls xml/schema/*.xsd`)
    xml val --err --xsd xml/schema/XMLSchema.xsd $file
end

# validate shaders
foreach file (`ls tests/shaders/*.xml`)
    xml val --err --xsd xml/schema/SBShader.xsd $file
end

# validate palettes 
foreach file (`ls tests/palettes/*.xml`)
    xml val --err --xsd xml/schema/SBPalette.xsd $file
end
