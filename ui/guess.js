const guess = function(){

	const ip = '192.168.1.15'
	const size = 28;
	pixel_size = 8

	console.log('guessing...')
	// get canva
	const canvas = document.getElementsByTagName('canvas')[0];
	const ctx = canvas.getContext("2d");
	const imgDataMultiColor = ctx.getImageData(0, 0, 28*8, 28*8).data;

	const imgData = []
	for (var i = 0; i<size*size*pixel_size*pixel_size; i++){
      imgData[i] = (255 - imgDataMultiColor[i*4])/3
      imgData[i] += (255 - imgDataMultiColor[i*4+1])/3
      imgData[i] += (255 - imgDataMultiColor[i*4+2])/3
    }

	var pixels = [];
	for(var i=0; i<size; i++) {
      for(var j=0; j<size; j++) {
        pixels[i*size+j] = 0;
        for(var di=0; di<pixel_size; di++){
          for(var dj=0; dj<pixel_size; dj++){
            const position = (i*pixel_size + di)*size*pixel_size + (j*pixel_size + dj)
            pixels[i*size+j] += imgData[position]/(pixel_size*pixel_size);
          }
        }
        // update the value of the div pixel
		const pixel_value = 255- pixels[i*size+j];
        const color = 'rgb('+pixel_value+','+pixel_value+','+pixel_value+')';
        document.getElementById('pixel_'+(i*size+j)).style.background = color;
      }
    }

	// send data to REST API
    pixels.unshift(0) // dummy guess not use but required in format. TODO: change this
//	const arr = { data :	     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,84,185,159,151,60,36,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,222,254,254,254,254,241,198,198,198,198,198,198,198,198,170,52,0,0,0,0,0,0,0,0,0,0,0,0,67,114,72,114,163,227,254,225,254,254,254,250,229,254,254,140,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,17,66,14,67,67,67,59,21,236,254,106,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,83,253,209,18,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,22,233,255,83,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,129,254,238,44,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,59,249,254,62,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,133,254,187,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,205,248,58,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,126,254,182,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,75,251,240,57,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,19,221,254,166,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,203,254,219,35,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,38,254,254,77,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,31,224,254,115,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,133,254,254,52,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,61,242,254,254,52,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,121,254,254,219,40,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,121,254,207,18,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}
 	const query = JSON.stringify({ data : pixels })
	fetch('http://'+ip+':5000/picture', {
      method: 'post',
      body: query,
	  headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json'
  	},
  	}).then(function(response) {
      return response.json();
    }).then(function(data) {
      const prediction = data.predictions
      console.log('guess:', data.predictions);
      update_content(prediction)
    }).catch(function(err){
	  console.log('error while sending request',err)
	});

	// change diplayed result
}

const update_content = function(prediction){
	const answer = document.getElementById('answer')
	answer.textContent = prediction
}
