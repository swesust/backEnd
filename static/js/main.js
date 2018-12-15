function closeLogin() {
	document.getElementById('login').style.display='none';
}
function showLogin() {
	document.getElementById('login').style.display='block';
}
function studentBtnClick() {
	document.getElementById('studentBtn').classList.add("activeType");
	document.getElementById('teacherBtn').classList.remove("activeType");
	document.getElementById('studentForm').classList.remove("hide");
	document.getElementById('teacherForm').classList.add("hide");
}
function teacherBtnClick() {
	document.getElementById('studentBtn').classList.remove("activeType");
	document.getElementById('teacherBtn').classList.add("activeType");
	document.getElementById('studentForm').classList.add("hide");
	document.getElementById('teacherForm').classList.remove("hide");
}