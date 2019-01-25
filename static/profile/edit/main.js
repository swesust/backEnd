function enableTo() {
    if(document.getElementById('stillWorkingChange').checked) {
        document.getElementById('endingDateChange').disabled=true;
    }
    else {
        document.getElementById('endingDateChange').disabled=false;
    }
}

enableTo();
enableWorkingBlock();

function enableWorkingBlock() {
    if(document.getElementById('hasWorkingBlock').checked) {
        document.getElementById('workingBlockContainer').style.display = 'block';
    }
    else {
        document.getElementById('workingBlockContainer').style.display = 'none';
    }
} 


function addEndrosement() {
	container = document.getElementById("endrosementContainer");
	form = document.getElementById("endrosementForm");

	container.append(form)
}