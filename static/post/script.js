function show() {
	document.querySelector(".pop-window").style.display = 'flex';
}

function hide() {
	document.querySelector(".pop-window").style.display = 'none';
}
window.onscroll = function() { scrollAction() };

function scrollAction() {
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
        document.getElementsByClassName('tab-section')[0].style.position = 'fixed';
        document.getElementsByClassName('tab-section')[0].style.marginTop = '-80px'
    }
    else{
        document.getElementsByClassName('tab-section')[0].style.position = 'relative';
        document.getElementsByClassName('tab-section')[0].style.marginTop = '80px'
    }
}


function showFull() {
    
}
