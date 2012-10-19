var terminal = {
    history: [],
    index: 0,

    store: function(arr) {
        this.history = arr;
        this.index = this.history.length;
        return this;
    },
    add: function(cmd) {
        this.history.push(cmd);
        this.index = this.history.length;
        return this;
    },

    listen: function() {
        var _this = this;
        syncrae.subscribe('/terminal/history/global', function(data) {
            _this.store(data.history);
        });
        syncrae.subscribe('/terminal/result', function(data) {
            if (result.cmd === true) {
                _this.add(data.log);
            }
        });
        return this;
    },

    // Usage functions
    next: function() {
        if (this.index == -1) {
            this.index = this.history.length;
        } else if (this.index < 0) {
            this.index = -1;
            return '';
        }
        this.index--;
        return this.history[this.index];
    },
    prev: function() {
        this.index++;
        if (this.index >= this.history.length) {
            this.index = -1;
            return '';
        }
        
        return this.history[this.index];
    },
    reset: function() {
        this.index = this.history.length;
        return this;
    }
};
terminal.listen();


$(function() {
    var searcher = {
        endpoint: '/api/terminal/search/',
        template: 'terminal-search',
        template_empty: 'terminal-search-empty',

        _request: false,
        _on: false,

        elem: function(elem) {
            this._elem = elem;
            return this;
        },
        request: function(val) {
            if (this._request !== false) {
                this._request.abort();
            }
            this.set_index(0);

            var _this = this;
            this._request = $.ajax(this.endpoint + val, {
                dataType: 'json',
                success: function(response) {
                    _this.render(response);
                },
                error: function(response) {
                    if (response.statusText != 'abort') {
                        console.error(response);
                    }
                }
            });
        },
        render: function(response) {
            this._elem.empty();

            if (!response.paging.length) {
                this._elem.append(Mustache.templates[this.template_empty](response.output));
            } else {
                var data = {'cmds': response.output};
                this._elem.append(Mustache.templates[this.template](data));
            }
        },

        // UI options
        _index: 0,
        up: function() {
            this.set_index(this._index + 1);
            return this;
        },
        down: function() {
            this.set_index(this._index - 1);
            return this;
        },
        set_index: function(val) {
            if (val < 0) {
                val = this._elem.children().length;
            } else if (val >= this._elem.children().length) {
                val = 0;
            }
            this._index = val;

            this._elem.find('.selected').removeClass('selected');
            this._elem.find(':nth-child(' + (val + 1) + ')').addClass('selected');
        },

        get_val: function() {
            return this._elem.find(':nth-child(' + (this._index + 1) + ')').data('value');
        },

        on: function() {


        }
    };

    input = $('#terminal-cmd');


    var obj = $.extend({}, result).elem(output);
    obj.refresh = function() {
        var val = input.val();
        if (val.length !== 0) {
            obj.request(val);
        }
    };

    input.on('change', function() {
        if (searcher._on) {
            obj.refresh();
        }
    });

    input.keyup(function(e) {
        var key = e.keyCode || window.event.keyCode;

        if (!searcher._on) {
            return;
        }

        // Up
        if (key == 38) {
            searcher.up();
            return false;
        // Down
        } else if (key == 40) {
            searcher.down();
            return false;
        // ESC
        } else if (key == 27) {
            searcher.off();
            return false;
        // Enter
        } else if (key ==13) {
            input.val(searcher.get_val())
        // Backspace, Delete, Space, A-Z
        } else if (key == 8 || key == 46 || key == 32 || (key >= 65 && key <= 90)) {
            obj.refresh();
        }
    });

    return obj;
});
