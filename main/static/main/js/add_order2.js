function catchSubmit(e) {
    let rooms = document.getElementsByName('roomclass');
    let foodtypes = document.getElementsByName('foodtype');
    let addservices = document.getElementsByName('addservicetypes');
    let cost = 0;

    for (let i = 0; i < rooms.length; ++i)
        if (rooms[i].checked) {
            cost = room_costs[i] * days;
            break;
        }

    for (let i = 0; i < foodtypes.length; ++i)
        if (foodtypes[i].checked) {
            cost += food_costs[i] * days * guests;
            break;
        }

    for (let i = 0; i < addservices.length; ++i)
        if (addservices[i].checked)
            cost += addservices_costs[i] * days;

    if (!confirm('Вы уверены, что хотите создать заказ? Его стоимость составит ' + cost + ' BYN!'))
        e.preventDefault();
}