/**
 * Finds any elements with the given selector
 * Including any current elements matching the selector
 */
$.fn.findi = function(selector) {
    return this.filter(selector).add(this.find(selector));
};
