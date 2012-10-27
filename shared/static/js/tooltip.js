inliner = (function() {
    var tooltip_elem;
    var func = function(val, elem) {
        inliner.get_elem();
        if (val === undefined) {
            val = 'hide';
        }
        if (val == 'hide') {
            tooltip_elem.removeClass('active');
            tooltip_elem.find('.form')
                .hide();
        } else if (val == 'show' && elem !== undefined) {
            inliner('hide');
            inliner.show(elem);
        }
    };
    func.shown = function(val) {
        return $('#tooltip').is(':visible');
    };

    func.get_elem = function() {
        if (tooltip_elem !== undefined) {
            return;
        } else {
            tooltip_elem = $('#tooltip');

            tooltip_elem.on('click', '.close', function() {
                inliner('hide');
            });
        }
    };
    func.show = function(elem) {
        tooltip_elem.find('.form#' + elem.data('inliner'))
            .show();

        var x = elem.offset().left;
        var y = elem.offset().top;
        tooltip_elem.removeClass('top bottom left right');

        if (x <= $(window).width() / 2) {
            tooltip_elem.addClass('right');
            x += 10;
        } else {
            tooltip_elem.addClass('left');
            x -= tooltip_elem.outerWidth() - 30;
        }

        if (y <= $(window).height() / 2) {
            tooltip_elem.addClass('bottom');
            y += tooltip_elem.outerHeight() - 20;
        } else {
            tooltip_elem.addClass('top');
            y -= tooltip_elem.outerHeight() + 10;
        }

        tooltip_elem.css('top', y);
        tooltip_elem.css('left', x);

        tooltip_elem.addClass('active');
    };

    return func;
})();

$(function() {
    $('#tooltip').on('click', function(event) {
        event.stopPropagation();
    });
    $(window).on('click', function() {
        if (inliner.shown()) {
            inliner('hide');
        }
    });
});


