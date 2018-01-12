const clearCanvas = function(){
	// clear all canvas to white

	console.log('clear');

	const canvas = document.getElementsByTagName('canvas')[0];
	const ctx = canvas.getContext("2d");
	ctx.clearTo("#FFFFFF");
};
