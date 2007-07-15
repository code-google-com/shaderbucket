surface simple(
	uniform color baseColour = 0;
	uniform float useTextures = 0;
	uniform string textureFile = "";
)
{
	color _C = 0;
	color _O = 0;
	
	_C = baseColour;
	if ( useTextures>0 && textureFile!="" )
		_C *= texture( textureFile, s, t );
	
	Oi = _O;
	Ci = _C * Oi;	
}
