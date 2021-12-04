$("#phonenumber").mask("+375 (99) 999-99-99", {autoclear: true});

function catchSubmit(e) {
    if (document.getElementById('passinput1').value !== document.getElementById('passinput2').value) {
        e.preventDefault();
        show_toast('Пароли не совпадают!', 'danger');
    }
}

function citizenship_other() {
    var select = document.getElementById('citizenship_select');
    var input = document.getElementById('citizenship_input');
    if (select.value === 'Другое') {
        select.required = false;
        select.name = 'citizenship1';
        input.innerHTML = "<input type=\"text\" name=\"citizenship\" placeholder=\"Гражданство\" class=\"textinput\" maxlength=\"30\" required>"
    } else {
        select.required = true;
        select.name = 'citizenship';
        input.innerHTML = "";
    }
}