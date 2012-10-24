// Terminal helper code

terminal = {};
terminal.elem = {
    input: function(elem) {
        this._elem = elem;
        this._text = elem.find('.user-cmd');
    },
    get: function() {
        return this._elem;
    },
    focus: function() {
        this._text.focus();
    },
    save: function() {
    }
};

terminal.history = History();

terminal.reloader = {
    elem: $(),

    reload: function() {
        terminal.elem.save();
        this.elem.focus();
        this.elem = $();
    },
    save: function(elem) {
        this.elem = elem;
        terminal.elem.focus();
    }
};

