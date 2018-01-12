const guess = function(){

	const size = 224;
	pixel_size = 8

	console.log('guessing...')
	// get canva
	const canvas = document.getElementsByTagName('canvas')[0];
	const ctx = canvas.getContext("2d");
	const imgData = ctx.getImageData(0, 0, size, size);
	console.log(imgData.data)

	var pixels = [];
	for(var i=0; i<size*size; i++) {
   	  pixels[i] = 0;
      for(var j=0; j<pixel_size; j++) {
        pixels[i] += 255 - imgData.data[i*pixel_size+j];
      }
	  pixels[i] /= pixel_size;
    }

	console.log(pixels)

	// send data to REST API

	// change diplayed result
}
