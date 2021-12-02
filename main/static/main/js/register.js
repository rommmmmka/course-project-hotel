$("#phonenumber").mask("+375 (99) 999-99-99", {autoclear: true});

function catchSubmit(e) {
    if (document.getElementById('passinput1').value !== document.getElementById('passinput2').value) {
        e.preventDefault();
        new Toast({
        title: false,
        text: 'Пароли не совпадают!',
        theme: 'danger',
        autohide: true,
        interval: 5000,
    });
    }
}