function enableTo() {
    if(document.getElementById('stillWorkingChange').checked) {
        document.getElementById('endingDateChange').disabled=true;
    }
    else {
        document.getElementById('endingDateChange').disabled=false;
    }
}

enableTo();
