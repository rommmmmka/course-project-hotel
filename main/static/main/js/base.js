function show_toast(text, theme, interval = 5000) {
    // Themes: danger, success, warning
    new Toast({
        title: false,
        text: text,
        theme: theme,
        autohide: true,
        interval: interval,
    });
}