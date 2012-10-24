// Terminal helper code

terminal = {};
terminal.elem = (function() {
    var term;
    var input;
    var wrapper = function get(arg) {
        if (arg === undefined) {
            return term;
        } else if (arg == 'text') {
            return input;
        } else {
            wrapper.input(arg);
        }
    };

    $.extend(wrapper, {
        input: function(elem) {
            term = elem;
            input = term.find('.user-cmd');
        }
    });

    return wrapper;
})();

terminal.history = History();

terminal.reloader = {
    elem: $(),

    reload: function() {
        this.elem.focus();
        this.elem = $();
    },
    save: function(elem) {
        this.elem = elem;
        terminal.elem('text').focus();
    }
};

