function catchSubmit(e) {
    if (document.getElementById('passinput1').value !== document.getElementById('passinput2').value) {
        e.preventDefault();
        show_toast('Пароли не совпадают!', 'danger');
    }
}
