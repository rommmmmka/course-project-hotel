var checkindate = document.getElementById('checkindate');
var checkoutdate = document.getElementById('checkoutdate');

Date.prototype.toDateInputValue = (function (add) {
    var local = new Date(this);
    local.setDate(local.getDate() + add);
    return local.toJSON().slice(0, 10);
});

checkindate.setAttribute('min', new Date().toDateInputValue(1));
checkoutdate.setAttribute('min', new Date().toDateInputValue(2));
checkindate.addEventListener('change', changeCheckOut)
checkoutdate.addEventListener('change', changeCheckIn)

function changeCheckIn() {
    console.log(checkoutdate.value)
    var date = new Date(checkoutdate.value);
    date.setDate(date.getDate() - 1);
    console.log(date);
    checkindate.setAttribute('max', date.toJSON().slice(0, 10));
}

function changeCheckOut() {
    var date = new Date(checkindate.value);
    date.setDate(date.getDate() + 1);
    checkoutdate.setAttribute('min', date.toJSON().slice(0, 10));
}
