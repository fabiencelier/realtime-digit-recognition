const clearCanvas = function(){
	// clear all canvas to white

	console.log('clear');


	const canvas = document.getElementsByTagName('canvas')[0];
	const ctx = canvas.getContext("2d");
	ctx.clearTo("#FFFFFF");

    // update the content of predictions to ?
    update_content('?');

    clearPixels();
	
};

const clearPixels = function(){

	const size = 28;
    const answer = document.getElementById('pixelized')

    // remove existing children
    while (answer.firstChild) {
      answer.removeChild(answer.firstChild);
    }

    // create new pixel matrix
    for( var i = 0; i < size; i++){
      const row = document.createElement("div");
      row.className = "row";
	  for ( var j = 0; j < size; j++){
        const pixel = document.createElement("div");
        pixel.className = "pixel";
		const id_number = i*size + j
        pixel.id = "pixel_"+id_number;
        pixel.style.background = 'white';
        row.appendChild(pixel);
      }
      answer.appendChild(row);
    }
}
