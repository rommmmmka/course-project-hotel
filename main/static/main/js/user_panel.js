let select_el = document.getElementById('select');

function rmorder(link) {
    if (confirm('Вы уверены, что хотите отменить заказ? Это действие нельзя будет отменить!'))
        window.location.href = link;
}

function playanim_active() {
    select_el.classList.add('anim_active');
}

function playanim_nonactive() {
    select_el.classList.add('anim_nonactive');
}
