
document.getElementById("id_current").addEventListener("change", enableTo);

function enableTo() {
	if(document.getElementById('id_current').checked) {
        document.getElementById('id_to_date').disabled=true;
    }
    else {
        document.getElementById('id_to_date').disabled=false;
    }
}

enableTo();