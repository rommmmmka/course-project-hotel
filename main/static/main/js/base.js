function show_toast(text, theme, interval = 5000) {
    // Темы: danger, success, warning
    new Toast({
        title: false,
        text: text,
        theme: theme,
        autohide: true,
        interval: interval,
    });
}

function catchSubmit(e) {
    if (document.getElementById('passinput1').value !== document.getElementById('passinput2').value) {
        e.preventDefault();
        show_toast('Пароли не совпадают!', 'danger');
    } else if (document.getElementById('passinput1').value === document.getElementById('passinputold').value) {
        e.preventDefault();
        show_toast('Старый и новый пароли не отличаются!', 'danger');
    }
}
