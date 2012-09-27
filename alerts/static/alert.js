var alerts = alerts || {};

alerts.click_close = function click_close(elem) {
    elem.on('click', function() {
        $(this).alert('close');
    });

    // Need a better cursor
    elem.css('cursor', 'not-allowed');

    return elem;
};

$(function() {
    alerts.click_close($('.alert.click-close'))

    var old_alert = $.fn.alert;

    $.fn.alert = function alert(opt) {
        // Hijack new alerts that have a close button
        if (opt === undefined && $(this).hasClass('click-close')) {
            alerts.click_close($(this));
        };
        return old_alert.call(this, opt);
    }
});
