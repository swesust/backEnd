function show() {
	document.querySelector(".new-post-create").style.display = 'none';
	document.querySelector(".pop-window").style.display = 'flex';
}

function hide() {
	document.querySelector(".new-post-create").style.display = 'inline-block';
	document.querySelector(".pop-window").style.display = 'none';
}