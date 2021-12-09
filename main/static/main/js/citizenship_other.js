$("#phonenumber").mask("+375 (99) 999-99-99", {autoclear: true});

function citizenship_other() {
    let select = document.getElementById('citizenship_select');
    let input = document.getElementById('citizenship_input');
    if (select.value === 'Другое') {
        select.required = false;
        select.name = 'citizenship1';
        input.innerHTML = "<input type=\"text\" name=\"citizenship\" placeholder=\"Гражданство\" class=\"textinput citizenshipinput\" maxlength=\"30\" required>"
    } else {
        select.required = true;
        select.name = 'citizenship';
        input.innerHTML = "";
    }
}
