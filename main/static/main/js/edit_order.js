function catchSubmit(e) {
    let foodtypes = document.getElementsByName('foodtype');
    let addservices = document.getElementsByName('addservicetypes');
    let cost = room_cost * days;

    for (let i = 0; i < foodtypes.length; ++i)
        if (foodtypes[i].checked) {
            cost += food_costs[i] * days * guests;
            break;
        }

    for (let i = 0; i < addservices.length; ++i)
        if (addservices[i].checked)
            cost += addservices_costs[i] * days;

    if (!confirm('Вы уверены, что хотите изменить заказ? Новая стоимость составит ' + cost + ' BYN!'))
        e.preventDefault();
}