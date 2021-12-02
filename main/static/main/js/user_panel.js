function rmorder(link) {
    console.log(link);
    if (confirm('Вы уверены, что хотите отменить заказ? Это действие нельзя будет отменить!')) {
        window.location.href = link;
    }
}