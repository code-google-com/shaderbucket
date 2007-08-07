surface simple(
	uniform color baseColour = 0;
	uniform float useTextures = 0;
	uniform string textureFile = "";
	
	uniform float basicFloat = 0.1;
	uniform string basicString = "some string";
	uniform float basicBool = 1;
	uniform string basicFile = "";
	uniform color basicColour = (1,0,0);
	uniform point basicPoint = (1,1,1);	
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
