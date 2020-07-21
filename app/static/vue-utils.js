


Vue.filter('decimal', function (valueOrig, minDig, maxDig) {
    if (valueOrig == null) {
        return '';
    }

    let value = valueOrig;
    if (typeof value === "string") {
        value = Number(value);
    }
    if (typeof value !== "number" || Number.isNaN(value)) {
        return valueOrig;
    }

    minDig = minDig === undefined ? 2 : minDig;
    maxDig = maxDig === undefined ? 2 : maxDig;

    var formatter = new Intl.NumberFormat('default', {
        minimumFractionDigits: minDig,
        maximumFractionDigits: maxDig
    });
    return formatter.format(value);
});




Vue.filter('date', function (value) {
    formatter = new Intl.DateTimeFormat('default')
    return value != null ? formatter.format(new Date(value)) : null;
});

Vue.filter('datetime', function (value) {
    var options = {year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric'};
    formatter = new Intl.DateTimeFormat('default', options)
    return value != null ? formatter.format(new Date(value)) : null;
});



