alignment = {
    moral: 50,
    order: 50,
    ratio: 2,

    elem: function(elem) {
        var _this = this;

        // The alignment container
        this.elem = elem;
        elem.find('.align-select-box').draggable({
            onstop: function(x, y) { return _this.pointer_stop(x, y); },
            onstart: function(x, y) { return _this.pointer_start(x, y); },
            onmove: function(x, y) { return _this.pointer_move(x, y); }
        });

        // The cursor on the alignment box
        this.pointer = elem.find('.align-pointer');

        return this;
    },
    update: function(order, moral) {
        this.order = order;
        this.moral = moral;
        this.refresh();
    },
    refresh: function() {
        this.elem.find('.align-moral')
            .val(this.moral);
        this.elem.find('.align-order')
            .val(this.order);
        var text = this.text();
        this.elem.find('.align-text')
            .val(text);

        this.pointer.css('top', (this.moral * this.ratio) - (this.pointer.width()) - 2 + 'px');
        this.pointer.css('left', (this.order * this.ratio) - (this.pointer.height() / 2) + 2 + 'px');
    },
    text: function() {
        var pre, suf;
        if (this.order >= 70) {
            pre = 'Lawful';
        } else if (this.order <= 30) {
            pre = 'Chaotic';
        } else {
            pre = 'True';
        }
        if (this.moral >= 70) {
            suf = 'Good';
        } else if (this.moral <= 30) {
            suf ='Evil';
        } else {
            suf = pre == 'True' ? 'Neutral' : pre;
            pre = 'True';
        }
        return pre + ' ' + suf;
    },
    read: function(string) {
        string = string.toLowerCase();
        moral = 50;
        order = 50;

        if ('chaotic' in string) {
            order = 30;
        } else if ('lawful' in string) {
            order = 70;
        }

        if ('good' in string) {
            moral = 30;
        } else if ('evil' in string) {
            moral = 70;
        }

        return {
            moral: moral,
            order: order
        };
    },
    events: function() {
        var _this = this;
        this.elem.find('.align-moral').on('change', function() {
            _this.update(_this.order, $(this).val());
        });
        this.elem.find('.align-order').on('change', function() {
            _this.update($(this).val(), _this.moral);
        });
        this.elem.find('.align-text').on('change', function() {
            var align = _this.read($(this).val());
            _this.update(align.order, align.moral);
        });
    },
    pointer_move: function(x, y) {
        this.update(Math.round(x / this.ratio), Math.round(y / this.ratio));
    },
    pointer_stop: function() {},
    pointer_start: function() {}
};
