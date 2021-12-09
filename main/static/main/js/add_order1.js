let checkindate = document.getElementById('checkindate');
let checkoutdate = document.getElementById('checkoutdate');

Date.prototype.toDateInputValue = (function (add) {
    let local = new Date(this);
    local.setDate(local.getDate() + add);
    return local.toJSON().slice(0, 10);
});

checkindate.setAttribute('min', new Date().toDateInputValue(1));
checkoutdate.setAttribute('min', new Date().toDateInputValue(2));
checkindate.addEventListener('change', changeCheckOut)
checkoutdate.addEventListener('change', changeCheckIn)

function changeCheckIn() {
    let date = new Date(checkoutdate.value);
    date.setDate(date.getDate() - 1);
    checkindate.setAttribute('max', date.toJSON().slice(0, 10));
}

function changeCheckOut() {
    let date = new Date(checkindate.value);
    date.setDate(date.getDate() + 1);
    checkoutdate.setAttribute('min', date.toJSON().slice(0, 10));
}
