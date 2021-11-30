var login_el = document.getElementById('login');
var emptyspace_el = document.getElementById('emptyspace');
var input_els = document.getElementsByClassName('textinput');
login_el.addEventListener('animationend', endanim);

$('a[href^="#"]').click(function () {
    let href = $(this).attr('href');
    $('html, body').animate({
        scrollTop: $(href).offset().top
    });
    playanim();
    return false;
});

function playanim() {
    login_el.classList.add('anim');
    emptyspace_el.classList.add('anim');
    input_els[0].classList.add('anim');
    input_els[1].classList.add('anim');
}

function endanim() {
    login_el.classList.remove('anim');
    emptyspace_el.classList.remove('anim');
    input_els[0].classList.remove('anim');
    input_els[1].classList.remove('anim');
}