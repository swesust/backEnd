
function facultyClicked(cb) {
    document.getElementsByName('regno')[0].value = "";
    document.getElementsByName('pass')[0].value = "";
    if (cb.checked) {
        document.getElementsByName('regno')[0].placeholder="Email";
    }
    else {
        document.getElementsByName('regno')[0].placeholder="Registration No";
    }
}
