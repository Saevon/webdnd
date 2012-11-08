/**
* Lightweight drag helper.  Handles containment within the element, so that
* when dragging, the x is within [0,element.width] and y is within [0,element.height]
* Taken from spectrum: http://bgrins.github.com/spectrum
*/
$.fn.draggable = function draggable(opts) {
    opts = opts || {};

    var element = this;
    var parent = opts.parent || element.parent();
    var onmove = opts.onmove || function() {};
    var onstart = opts.onstart || function() {};
    var onstop = opts.onstop || function() {};

    var doc = element.ownerDocument || document;
    var dragging = false;
    var offset = {};
    var maxHeight = 0;
    var maxWidth = 0;
    var IE = $.browser.msie;
    var hasTouch = ('ontouchstart' in window);

    var duringDragEvents = {};
    duringDragEvents["selectstart"] = prevent;
    duringDragEvents["dragstart"] = prevent;
    duringDragEvents[(hasTouch ? "touchmove" : "mousemove")] = move;
    duringDragEvents[(hasTouch ? "touchend" : "mouseup")] = stop;

    function prevent(e) {
        if (e.stopPropagation) {
            e.stopPropagation();
        }
        if (e.preventDefault) {
            e.preventDefault();
        }
        e.returnValue = false;
    }

    function move(e) {
        if (dragging) {
            // Mouseup happened outside of window
            if (IE && document.documentMode < 9 && !e.button) {
                return stop();
            }

            var touches = e.originalEvent.touches;
            var pageX = touches ? touches[0].pageX : e.pageX;
            var pageY = touches ? touches[0].pageY : e.pageY;

            var dragX = Math.max(0, Math.min(pageX - offset.left, maxWidth));
            var dragY = Math.max(0, Math.min(pageY - offset.top, maxHeight));

            if (hasTouch) {
                // Stop scrolling in iOS
                prevent(e);
            }

            onmove.apply(element, [dragX, dragY, e]);
        }
    }
    function start(e) {
        var rightclick = (e.which) ? (e.which == 3) : (e.button == 2);
        var touches = e.originalEvent.touches;

        if (!rightclick && !dragging) {
            if (onstart.apply(element, arguments) !== false) {
                dragging = true;
                maxHeight = element.height();
                maxWidth = element.width();
                offset = element.offset();

                $(doc).bind(duringDragEvents);
                parent.addClass("sp-dragging");

                if (!hasTouch) {
                    move(e);
                }

                prevent(e);
            }
        }
    }
    function stop() {
        if (dragging) {
            $(doc).unbind(duringDragEvents);
            parent.removeClass("sp-dragging");
            onstop.apply(element, arguments);
        }
        dragging = false;
    }

    element.bind(hasTouch ? "touchstart" : "mousedown", start);

    return this;
};
$.fn.draggable.load = true;
$.fn.draggable.loadOpts = {};
$.fn.draggable.defaults = {};

