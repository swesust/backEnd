
window.onscroll = function() { scrollAction() };

function scrollAction() {
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
        document.getElementsByClassName('tab-section')[0].style.position = 'fixed';
        document.getElementsByClassName('tab-section')[0].style.marginTop = '-40px';
    }
    else{
        document.getElementsByClassName('tab-section')[0].style.position = 'relative';
        document.getElementsByClassName('tab-section')[0].style.marginTop = '80px'
    }
}
